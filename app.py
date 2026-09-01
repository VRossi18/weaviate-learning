import streamlit as st
import weaviate.classes as wvc
from weaviate.util import generate_uuid5

client = wvc.Client("http://localhost:8080")

try: 
    movies = client.collections.get("Movie")
    synopses = client.collections.get("Synopsis")

    st.title("ReelRecommender")

    search_tab, movie_tab, rec_tab = st.tabs(["Search", "Movie details", "Recommend"])

    with search_tab:

        st.header("Search for a movie")
        query_string = st.text_input(label="Search for a movie")

        srch_col1, srch_col2 = st.columns(2)
        with srch_col1:
            search_type = st.radio(
                label="How do you want to search?",
                options=["Vector", "Hybrid"]
            )

        with srch_col2:
            value_range = st.slider(label="Rating range", value=(0.0, 5.0), step=0.1)

        st.header("Search results")

        movie_filter = (
            wvc.query.Filter.by_property("rating").greater_or_equal(value_range[0])
            & wvc.query.Filter.by_property("rating").less_or_equal(value_range[1])
        )
        synopsis_xref = wvc.query.QueryReference(
            link_on="hasSynopsis", return_properties=["body"]
        )

        if len(query_string) > 0: 

            if search_type == "Vector":
                response = movies.query.near_text(
                    query=query_string,
                    filters=movie_filter,
                    limit=5,
                    return_references=[synopsis_xref],
                )
            else:
                response = movies.query.hybrid(
                    query=query_string,
                    filters=movie_filter,
                    limit=5,
                    return_references=[synopsis_xref],
                )
        else:
            response = movies.query.fetch_objects(
                filters=movie_filter,
                limit=5,
                return_references=[synopsis_xref],
            )

        for movie in response.objects:
            with st.expander(movie.properties["title"]):
                rating = movie.properties["rating"]
                movie_id = movie.properties["movie_id"]
                st.write(f"**Movie rating**: {rating}, **ID**: {movie_id}")

                synopsis = movie.references["hasSynopsis"].objects[0].properties["body"]
                st.write("**Synopsis**")
                st.write(synopsis[:200] + "...")


    with movie_tab:

        st.header("Movie details")
        title_input = st.text_input(label="Enter the movie row ID here (0-120)", value="")
        if len(title_input) > 0: 
            movie_uuid = generate_uuid5(int(title_input))

            movie = movies.query.fetch_object_by_id(
                uuid=movie_uuid,
                return_references=[
                    wvc.query.QueryReference(
                        link_on="hasSynopsis", return_properties=["body"]
                    ),
                ],
            )

            title = movie.properties["title"]
            director = movie.properties["director"]
            rating = movie.properties["rating"]
            movie_id = movie.properties["movie_id"]
            year = movie.properties["year"]

            st.header(title)
            st.write(f"Director: {director}")
            st.write(f"Rating: {rating}")
            st.write(f"Movie ID: {movie_id}")
            st.write(f"Year: {year}")

            with st.expander("See synopsis"):
                st.write(movie.references["hasSynopsis"].objects[0].properties["body"])


    with rec_tab:
        st.header("Recommend me a movie")
        search_string = st.text_input(label="Recommend me a ...", value="")
        occasion = st.text_input(label="In this context ...", value="any occasion")

        if len(search_string) > 0 and len(occasion) > 0:
            st.subheader("Recommendations")

            response = synopses.generate.hybrid(
                query=search_string,
                grouped_task=f"""
                The user is looking to watch
                {search_string} types of movies for {occasion}.
                Provide a movie recommendation
                based on the provided movie synopses.
                """,
                limit=3,
                return_references=[
                    wvc.query.QueryReference(
                        link_on="forMovie", return_properties=["title", "movie_id", "description"]
                    ),
                ],
            )

            st.write(response.generated)

            st.subheader("Movies analysed")
            for i, m in enumerate(response.objects):
                movie_title = m.references["forMovie"].objects[0].properties["title"]
                movie_id = m.references["forMovie"].objects[0].properties["movie_id"]
                movie_description = m.references["forMovie"].objects[0].properties["description"]
                with st.expander(f"Movie title: {movie_title}, ID: {movie_id}"):
                    st.write(movie_description)
finally:
    client.close()  