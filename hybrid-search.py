import requests, json
import weaviate 

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

response = client.query.get("Question", ["question", "answer", "category"]).with_hybrid(query="animal", alpha=0.5).with_limit(3).do()

print(json.dumps(response, indent=2))