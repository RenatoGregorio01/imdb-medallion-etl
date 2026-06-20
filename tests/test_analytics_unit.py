import pandas as pd


def test_genre_statistics_schema() -> None:

    df = pd.read_parquet("data/gold/analytics/genre_statistics.parquet")

    expected = {
        "genre_name",
        "movie_count",
        "avg_rating",
        "total_votes",
    }

    assert set(df.columns) == expected


def test_yearly_statistics_schema() -> None:

    df = pd.read_parquet("data/gold/analytics/yearly_movie_statistics.parquet")

    expected = {
        "year",
        "movie_count",
        "avg_rating",
        "avg_runtime",
        "total_votes",
    }

    assert set(df.columns) == expected
