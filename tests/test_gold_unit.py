import pandas as pd

from src.transform.gold import (
    create_bridge_movie_genre,
    create_fact_movie,
)


def test_create_fact_movie() -> None:

    df = pd.DataFrame(
        {
            "average_rating": [8.5],
            "num_votes": [1000],
        }
    )

    dim_movie = pd.DataFrame(
        {
            "movie_key": [1],
        }
    )

    result = create_fact_movie(
        df,
        dim_movie,
    )

    assert len(result) == 1

    assert result.loc[0, "movie_key"] == 1

    assert result.loc[0, "average_rating"] == 8.5

    assert result.loc[0, "num_votes"] == 1000


def test_create_bridge_movie_genre() -> None:

    df = pd.DataFrame({"genres": ["Action,Drama"]})

    dim_movie = pd.DataFrame({"movie_key": [1]})

    dim_genre = pd.DataFrame(
        {
            "genre_key": [1, 2],
            "genre_name": [
                "Action",
                "Drama",
            ],
        }
    )

    result = create_bridge_movie_genre(
        df,
        dim_movie,
        dim_genre,
    )

    assert len(result) == 2

    assert set(result["genre_key"]) == {1, 2}
