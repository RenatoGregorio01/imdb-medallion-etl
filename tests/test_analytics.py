import pandas as pd


def test_genre_statistics_not_empty(
    genre_statistics_df: pd.DataFrame,
) -> None:
    assert not genre_statistics_df.empty


def test_yearly_statistics_not_empty(
    yearly_movie_statistics_df: pd.DataFrame,
) -> None:
    assert not yearly_movie_statistics_df.empty


def test_genre_statistics_columns(
    genre_statistics_df: pd.DataFrame,
) -> None:

    expected = {
        "genre_name",
        "movie_count",
        "avg_rating",
        "total_votes",
    }

    assert set(genre_statistics_df.columns) == expected


def test_yearly_statistics_columns(
    yearly_movie_statistics_df: pd.DataFrame,
) -> None:

    expected = {
        "year",
        "movie_count",
        "avg_rating",
        "avg_runtime",
        "total_votes",
    }

    assert set(yearly_movie_statistics_df.columns) == expected
