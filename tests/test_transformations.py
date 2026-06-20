import pandas as pd

from src.transform.gold import (
    create_dim_genre,
    create_dim_movie,
)

from src.transform.silver import (
    normalize_genres,
)


def test_normalize_genres_with_spaces() -> None:

    result = normalize_genres("Action, Drama")

    assert result == "Action,Drama"


def test_normalize_genres_extra_spaces() -> None:

    result = normalize_genres("Action , Drama")

    assert result == "Action,Drama"


def test_normalize_genres_null() -> None:
    assert normalize_genres(None) == "Unknown"


def test_create_dim_movie() -> None:

    df = pd.DataFrame(
        {
            "imdb_id": ["tt0001"],
            "title": ["Movie"],
            "original_title": ["Movie"],
            "year": [2020],
            "runtime_minutes": [120],
            "imdb_url": ["https://imdb.com"],
        }
    )

    result = create_dim_movie(df)

    assert len(result) == 1

    assert (
        result.loc[
            0,
            "movie_key",
        ]
        == 1
    )

    assert (
        result.loc[
            0,
            "imdb_id",
        ]
        == "tt0001"
    )


def test_create_dim_genre() -> None:

    df = pd.DataFrame(
        {
            "genres": [
                "Action,Drama",
                "Drama,Comedy",
            ]
        }
    )

    result = create_dim_genre(df)

    assert len(result) == 3

    assert set(result["genre_name"]) == {
        "Action",
        "Comedy",
        "Drama",
    }


def test_create_dim_genre_keys_are_unique() -> None:

    df = pd.DataFrame(
        {
            "genres": [
                "Action,Drama",
                "Drama,Comedy",
            ]
        }
    )

    result = create_dim_genre(df)

    assert result["genre_key"].is_unique
