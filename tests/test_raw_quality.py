import pandas as pd


def test_imdb_id_unique() -> None:

    df = pd.read_csv(
        "data/raw/imdb_top_movies_1980_2026.csv"
    )

    assert (
        df["imdb_id"]
        .duplicated()
        .sum()
        == 0
    )


def test_rating_range() -> None:

    df = pd.read_csv(
        "data/raw/imdb_top_movies_1980_2026.csv"
    )

    assert (
        df["average_rating"]
        .between(0, 10)
        .all()
    )


def test_year_range() -> None:

    df = pd.read_csv(
        "data/raw/imdb_top_movies_1980_2026.csv"
    )

    assert (
        df["year"]
        .between(1980, 2026)
        .all()
    )
    