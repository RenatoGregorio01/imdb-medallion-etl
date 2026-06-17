from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.utils.logger import logger

RAW_FILE = Path(
    "data/raw/imdb_top_movies_1980_2026.csv"
)

BRONZE_FILE = Path(
    "data/bronze/movies_raw.parquet"
)


def create_bronze_layer(
    force_refresh: bool = False,
) -> None:
    try:
        logger.info(
            "[BRONZE] Iniciando geração da camada Bronze"
        )

        if not RAW_FILE.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {RAW_FILE}"
            )

        # Idempotência
        if (
            BRONZE_FILE.exists()
            and not force_refresh
        ):
            logger.info(
                "[BRONZE] Arquivo já existe: {}",
                BRONZE_FILE,
            )
            return

        logger.info(
            "[BRONZE] Lendo arquivo CSV"
        )

        df = pd.read_csv(
            RAW_FILE,
            dtype={
                "imdb_id": "string",
                "title": "string",
                "original_title": "string",
                "genres": "string",
                "imdb_url": "string",
            },
        )

        logger.info(
            "[BRONZE] {} registros carregados",
            len(df)
        )

        # Metadados técnicos
        df["_ingestion_timestamp"] = (
            datetime.now(timezone.utc)
        )

        df["_source"] = "kaggle"

        BRONZE_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        logger.info(
            "[BRONZE] Salvando arquivo Parquet"
        )

        df.to_parquet(
            BRONZE_FILE,
            engine="pyarrow",
            index=False,
        )

        logger.success(
            "[BRONZE] Camada Bronze criada com sucesso"
        )

    except Exception:
        logger.exception(
            "[BRONZE] Erro ao gerar camada Bronze"
        )
        raise
    