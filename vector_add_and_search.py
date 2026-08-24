import requests
import json
import weaviate 
from weaviate import EmbeddedOptions 
import os

repons = request.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
data = []
client = weaviate.Client(embedded_options=EmbeddedOptions(), additional_headers={"X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]})

if client.schema.exists("Question"):
    client.schema.delete_class("Question")

class_obj = {
    "class": "Question",
    "vectorizer": "text2vec-openai"
}

client.schema.create_class(class_obj)

with client.batch.configure() as batch:
    for i, d in enumerate(data):
        print(f"importing question: {i+1}") 
        properties = {
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Catergory"]
        }

        batch.add_data_object(
            data_object=properties,
            class_name="Question"
        )

json_print(client.query.aggregate("Question").with_meta_count().do())

result = (client.query
          .get("Question", ["category", "question", "answer"])
          .with_additional("vector")
          .with_limit(1)
          .do())

print(result['data']['Get']['Question'][0]['question'])
## Vectors that answer the question
print(result['data']['Get']['Question'][0]['_additional']['vector'])

response = (client.query
            .get("Question", ["question","answer","category"])
            .with_near_text({"concepts": ["biology"], "distance": 0.24})
            .with_additional("distance")
            .with_limit(2)
            .do())