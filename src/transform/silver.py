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


def normalize_genres(value: str | None) -> str:
    """
    Padroniza a coluna de gêneros.

    Exemplos:
    - "Action, Adventure" -> "Action,Adventure"
    - "Action , Adventure" -> "Action,Adventure"
    - None -> "Unknown"
    """

    if pd.isna(value):
        return "Unknown"

    genres = [
        genre.strip()
        for genre in value.split(",")
    ]

    return ",".join(genres)


def create_silver_layer(
    force_refresh: bool = False,
) -> None:
    try:
        logger.info(
            "[SILVER] Iniciando camada Silver"
        )

        if not BRONZE_FILE.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {BRONZE_FILE}"
            )

        # Idempotência
        if (
            SILVER_FILE.exists()
            and not force_refresh
        ):
            logger.info(
                "[SILVER] Arquivo já existe: {}",
                SILVER_FILE
            )
            return

        df = pd.read_parquet(
            BRONZE_FILE
        )

        logger.info(
            "[SILVER] {} registros carregados",
            len(df)
        )

        initial_count = len(df)

        # Remove registros sem imdb_id
        df = df[
            df["imdb_id"].notna()
        ]

        # Remove duplicados
        df = df.drop_duplicates(
            subset=["imdb_id"]
        )

        # Padroniza gêneros
        df["genres"] = df["genres"].apply(
            normalize_genres
        )

        # Conversão de tipos
        df["year"] = df["year"].astype(
            "Int64"
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

        # Validação do ano
        df = df[
            df["year"].between(
                1980,
                2026
            )
        ]

        # Validação da nota
        df = df[
            df["average_rating"].between(
                0,
                10
            )
        ]

        # Validação da URL
        df = df[
            df["imdb_url"].str.startswith(
                "https://www.imdb.com/title/"
            )
        ]

        final_count = len(df)

        logger.info(
            "[SILVER] Registros removidos: {}",
            initial_count - final_count
        )

        df["_silver_timestamp"] = (
            datetime.now(
                timezone.utc
            )
        )

        SILVER_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        logger.info(
            "[SILVER] Salvando arquivo Parquet"
        )

        df.to_parquet(
            SILVER_FILE,
            engine="pyarrow",
            index=False
        )

        logger.success(
            "[SILVER] Camada Silver criada com sucesso"
        )

        logger.info(
            "[SILVER] Total de registros: {}",
            len(df)
        )

    except Exception:
        logger.exception(
            "[SILVER] Erro na camada Silver"
        )
        raise
    