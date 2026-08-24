import requests
import json
import weaviate 
from weaviate import EmbeddedOptions 
import os

resp = request.get('https://raw.githubusercontent.com/weaviate-tutorials/intro-workshop/main/data/jeopardy_1k.json')
data = json.loads(resp.text)

client = weaviate.Client(embedded_options=EmbeddedOptions(), additional_headers={"X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]})

if client.schema.exists("Question"):
    client.schema.delete_class("Question")

class_obj = {
    "class": "Question",
    "vectorizer": "text2vec-openai",
    "vectorIndexConfig": {
        "distance": "cosine"
    },
    "propertires": [
        {
            "name": "question",
            "dataType": ['text']
        },
        {
            "name": "answer"
            "dataType": ['text']
        },
        {
            "name": "round",
            "dataType": ['text']
        }
    ]
}

client.schema.create_class(class_obj)

with client.batch.configure() as batch:
    for i, d in enumerate(data):
        properties = {
            "question": d["Question"],
            "answer": d["Answer"],
            "round": d["Round"]
        }

        batch.add_data_object(
            data_object=properties,
            class_name="Question"
        )

print(json.dumps(client.query.aggregate("Question").with_meta_count().do()), indent=2)

##spicy foods
spicy_foods = (client.query
                    .get("Question", ["question", "answer", "round"])
                    .with_near_text("concepts": "spicy foods recipe")
                    .with_additional(['distance'])
                    .with_limit(4)
                    .do())

