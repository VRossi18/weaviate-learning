import pickle, weaviate, json, os, IPython

client = weaviate.Client("http://localhost:8080")
print(f"Client created? {client.is_ready()}")

class_obj = {
    "class": "Challenge3",
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
    encoded_image = weaviate.util.image_encoder_b64(f'Images/{img}')
    data_properties = {
        "image": encoded_image,
        "text": img
    }

    client.data_object.create(data_properties, "Challenge3")

print(f"All images processed")

res = (client.query.get("Challenge3", ["text", "_additional {distance}"]).with_near_text({"concepts": "a photo of a cat"}).with_limit(5).do())
print(json.dumps(res, indent=2))

res_img = (client.query.get("Challenge3", ["text", "_additional {distance}"]).with_near_image({"image": "TestImages/Alone in office building _LIL_134159.jpg"}).with_limit(1).do())
print(json.dumps(res_img, indent=2))

IPython.display.Image(filename=f"TestImages/Alone in office building _LIL_134159.jpg", width=300)
IPython.display.Image(filename=f"Images/{res_img['data']['Get']['Challenge3'][0]['text']}", width=300)