from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture(scope="session")
def silver_df() -> pd.DataFrame:
    return pd.read_parquet(
        Path(
            "data/silver/movies_clean.parquet"
        )
    )


@pytest.fixture(scope="session")
def dim_movie_df() -> pd.DataFrame:
    return pd.read_parquet(
        Path(
            "data/gold/dim_movie.parquet"
        )
    )


@pytest.fixture(scope="session")
def dim_genre_df() -> pd.DataFrame:
    return pd.read_parquet(
        Path(
            "data/gold/dim_genre.parquet"
        )
    )


@pytest.fixture(scope="session")
def fact_movie_df() -> pd.DataFrame:
    return pd.read_parquet(
        Path(
            "data/gold/fact_movie.parquet"
        )
    )


@pytest.fixture(scope="session")
def bridge_movie_genre_df() -> pd.DataFrame:
    return pd.read_parquet(
        Path(
            "data/gold/bridge_movie_genre.parquet"
        )
    )


@pytest.fixture(scope="session")
def genre_statistics_df() -> pd.DataFrame:
    return pd.read_parquet(
        Path(
            "data/gold/analytics/genre_statistics.parquet"
        )
    )


@pytest.fixture(scope="session")
def yearly_movie_statistics_df() -> pd.DataFrame:
    return pd.read_parquet(
        Path(
            "data/gold/analytics/yearly_movie_statistics.parquet"
        )
    )
