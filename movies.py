import weaviate.classes as wvc

client = wvc.Client("http://localhost:8080")

client.collections.create(
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
)

client.close()