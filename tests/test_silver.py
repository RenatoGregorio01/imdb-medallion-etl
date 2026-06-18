import pandas as pd


def test_imdb_id_is_unique(
    silver_df: pd.DataFrame,
) -> None:
    assert silver_df[
        "imdb_id"
    ].is_unique


def test_average_rating_range(
    silver_df: pd.DataFrame,
) -> None:
    assert silver_df[
        "average_rating"
    ].between(
        0,
        10,
    ).all()


def test_year_range(
    silver_df: pd.DataFrame,
) -> None:
    assert silver_df[
        "year"
    ].between(
        1980,
        2026,
    ).all()


def test_imdb_url_format(
    silver_df: pd.DataFrame,
) -> None:
    assert silver_df[
        "imdb_url"
    ].str.startswith(
        "https://www.imdb.com/title/"
    ).all()
    