from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.utils.logger import logger

BRONZE_FILE = Path(
    "data/bronze/movies_raw.parquet"
)

SILVER_FILE = Path(
    "data/silver/movies_clean.parquet"
)


def create_silver_layer() -> None:
    try:
        logger.info(
            "[SILVER] Iniciando camada Silver"
        )

        df = pd.read_parquet(
            BRONZE_FILE
        )

        logger.info(
            "[SILVER] {} registros carregados",
            len(df)
        )

        # Remove IDs nulos
        df = df[
            df["imdb_id"].notna()
        ]

        # Remove duplicados
        df = df.drop_duplicates(
            subset=["imdb_id"]
        )

        # Trata gêneros nulos
        df["genres"] = (
            df["genres"]
            .fillna("Unknown")
        )

        # Conversão de tipos
        df["year"] = (
            df["year"]
            .astype("Int64")
        )

        df["runtime_minutes"] = (
            df["runtime_minutes"]
            .astype("Int64")
        )

        df["num_votes"] = (
            df["num_votes"]
            .astype("Int64")
        )

        df["average_rating"] = (
            df["average_rating"]
            .astype(float)
        )

        # Valida ano
        df = df[
            df["year"].between(
                1980,
                2026
            )
        ]

        # Valida nota
        df = df[
            df["average_rating"].between(
                0,
                10
            )
        ]

        # Valida URL
        df = df[
            df["imdb_url"].str.startswith(
                "https://www.imdb.com/title/"
            )
        ]

        # Metadado técnico
        df["_silver_timestamp"] = (
            datetime.now(
                timezone.utc
            )
        )

        SILVER_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_parquet(
            SILVER_FILE,
            engine="pyarrow",
            index=False
        )

        logger.success(
            "[SILVER] Camada Silver criada com sucesso"
        )

    except Exception:
        logger.exception(
            "[SILVER] Erro na camada Silver"
        )
        raise
    