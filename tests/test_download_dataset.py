from pathlib import Path

import pandas as pd

RAW_FILE = Path("data/raw/imdb_top_movies_1980_2026.csv")


def test_raw_file_exists() -> None:
    assert RAW_FILE.exists()


def test_raw_file_not_empty() -> None:

    df = pd.read_csv(RAW_FILE)

    assert len(df) > 0


def test_raw_expected_columns() -> None:

    df = pd.read_csv(RAW_FILE)

    expected_columns = {
        "imdb_id",
        "title",
        "original_title",
        "year",
        "runtime_minutes",
        "genres",
        "average_rating",
        "num_votes",
        "imdb_url",
    }

    assert set(df.columns) == expected_columns
