import pandas as pd


def test_movie_key_is_unique(
    dim_movie_df: pd.DataFrame,
) -> None:
    assert dim_movie_df["movie_key"].is_unique


def test_genre_key_is_unique(
    dim_genre_df: pd.DataFrame,
) -> None:
    assert dim_genre_df["genre_key"].is_unique


def test_fact_movie_fk(
    fact_movie_df: pd.DataFrame,
    dim_movie_df: pd.DataFrame,
) -> None:

    assert set(fact_movie_df["movie_key"]).issubset(set(dim_movie_df["movie_key"]))


def test_bridge_movie_fk(
    bridge_movie_genre_df: pd.DataFrame,
    dim_movie_df: pd.DataFrame,
) -> None:

    assert set(bridge_movie_genre_df["movie_key"]).issubset(
        set(dim_movie_df["movie_key"])
    )


def test_bridge_genre_fk(
    bridge_movie_genre_df: pd.DataFrame,
    dim_genre_df: pd.DataFrame,
) -> None:

    assert set(bridge_movie_genre_df["genre_key"]).issubset(
        set(dim_genre_df["genre_key"])
    )
