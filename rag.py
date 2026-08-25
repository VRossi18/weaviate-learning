import requests, json
import weaviate

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"

resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/intro-workshop/main/data/jeopardy_1k.json')
data = json.loads(resp.text)

client = weaviate.Client("http://localhost:8080")

if client.schema.exists("Question"):
    client.schema.delete_class("Question")

class_obj = {
    "class": "Question",
    "vectorizer": "text2vec-contextionary",
}

client.schema.create_class(class_obj)

with client.batch.configure() as batch:
    for i, d in enumerate(data):
        print(f"importing question: {i+1}")
        properties = {
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"]
        }

        batch.add_data_object(
            data_object=properties,
            class_name="Question"
        )

response = client.query.get("Question", ["answer"]).with_near_text({"concepts": ["animal"]}).with_limit(3).do()
print(json.dumps(response, indent=2))

hits = (
    client.query.get("Question", ["answer"])
    .with_near_text({"concepts": ["animal"]})
    .with_limit(2)
    .do()
)

answers = [obj["answer"] for obj in hits["data"]["Get"]["Question"]]
prompt = f"Tell me a story about this animal {answers[0]} flying"

llm_response = requests.post(
    OLLAMA_URL,
    json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
    timeout=120,
)
llm_response.raise_for_status()
print(llm_response.json()["response"])
