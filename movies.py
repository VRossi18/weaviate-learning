import weaviate.classes as wvc
import pandas as pd
import uuid
from typing import List

client = wvc.Client("http://localhost:8080")

reviews = client.collections.create(
    name="reviews",
    vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_contextionary(),
    generative_config=wvc.config.Configure.Generative.openai(),
    properties=[
        wvc.config.Property(
            name="body",
            data_type=wvc.config.DataType.TEXT,
        )
    ]
)

synopsis = client.collections.create(
    name="synopsis",
    vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_contextionary(),
    generative_config=wvc.config.Configure.Generative.openai(),
    properties=[
        wvc.config.Property(
            name="body",
            data_type=wvc.config.DataType.TEXT,
        )
    ]
)

movies = client.collections.create(
    name="movies",
    vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_contextionary(),
    generative_config=wvc.config.Configure.Generative.openai(),
    properties=[
        wvc.config.Property(
            name="title",
            data_type=wvc.config.DataType.STRING,
        ),
        wvc.config.Property(
            name="description",
            data_type=wvc.config.DataType.STRING,
        ),
        wvc.config.Property(
            name="movie_id",
            data_type=wvc.config.DataType.INT,
        ),
        wvc.config.Property(
            name="year",
            data_type=wvc.config.DataType.INT,
        ),
        wvc.config.Property(
            name="rating",
            data_type=wvc.config.DataType.NUMBER,
        ),
        wvc.config.Property(
            name="director",
            data_type=wvc.config.DataType.STRING,
            skip_vectorization=True,
        )
    ],

    references=[
        wvc.config.ReferenceProperty(
            name="hasReview",
            target_collection=reviews.name
        )
    ]
)

movies.config.add_reference(
    name="hasReview",
    target_collection=reviews.name
)

movie_df = pd.read_csv("movies.csv")
movie_df.head()

movie_objects = List()
for index, row in movie_df.iterrows():
    movie_uuid = str(uuid.uuid4())

    prop = {
        "title": row["title"],
        "description": row["description"],
        "year": row["year"],
        "rating": row["rating"],
        "director": row["director"],
    }

    data_obj = wvc.data.DataObject(
        properties=prop,
        uuid=movie_uuid,
    )
    movie_objects.append(data_obj)
    
response = movies.data.insert_many(movie_objects)

client.close()