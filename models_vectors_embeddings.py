import weaviate, json, os, IPython

client = weaviate.Client("http://localhost:8080")
print(f"Client created? {client.is_ready()}")

current_schemas = client.schema.get()['classes']

for schema in current_schemas:
    if schema['class'] == 'ClipExample':
        client.schema.delete_class('ClipExample')

class_obj = {
    "class": "ClipExample",
    "moduleConfig": {
        'multi2vec-clip': { 
            "imageFields": ["image"]
        },
    "vectorizer": "multi2vec-clip",
    "properties": [{ "name": "text", "dataType": "string"}, { "name": "image", "dataType": "blob"}]
    }
}

client.schema.create_class(class_obj)
print(f"Class created? {client.schema.get()}")

for img in os.listdir("Images/"):
    print(f"Processing {img}")

    encoded_image = weaviate.util.image_encoder_b64(f"Images/{img}")

    data_properties = {
        "image": encoded_image,
        "text": img
    }

    client.data_object.create(data_properties, "ClipExample")

print(f"All images processed")

res = (client.query.get("ClipExample", ['text', '_additional {distance}'])
        .with_near_text({"concepts": "open sea beach"})
        .with_limit(5)
        .do())

print(json.dumps(res, indent=2))
