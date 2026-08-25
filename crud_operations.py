import requests, json
import weaviate 
from weaviate import EmbeddedOptions 
import os

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

uuid = client.data_object.create(
    data_object = {
        'quesiton': "Leonardo da vinci was born in this country",
        'answer': "Italy",
        'category': 'Culture'
    },
    class_name="Question"
)

client.data_object.update(uuid=uuid, class_name="Question", data_object={'answer': 'Florence, Italy'})

data_object = client.data_object.get_by_id(uuid, class_name="Question", with_vector=True)
print(json.dumps(data_object, indent=2))

client.data_object.delete(uuid=uuid, class_name="Question")
print(f"Object deleted with UUID: {uuid}")