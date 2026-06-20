import os
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
from src.utils.logger import logger

BASE_DATA_DIR = Path(os.getenv("AIRFLOW_DATA_DIR", "data"))

RAW_FILE = BASE_DATA_DIR / "raw/imdb_top_movies_1980_2026.csv"
BRONZE_FILE = BASE_DATA_DIR / "bronze/movies_raw.parquet"


def create_bronze_layer(force_refresh: bool = False, **kwargs) -> None:
    """
    Cria a camada Bronze transformando o CSV de origem em Parquet.
    """
    try:
        logger.info("[BRONZE] Iniciando geração da camada Bronze")

        # Garantir que os diretórios existam antes de qualquer operação
        RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
        BRONZE_FILE.parent.mkdir(parents=True, exist_ok=True)

        if not RAW_FILE.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {RAW_FILE}")

        # Idempotência: verifica se o arquivo já existe e se não deve ser forçado o refresh
        if BRONZE_FILE.exists() and not force_refresh:
            logger.info(
                "[BRONZE] Arquivo já existe: {}. Pulando processamento.", BRONZE_FILE
            )
            return

        logger.info("[BRONZE] Lendo arquivo CSV: {}", RAW_FILE)

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

        logger.info("[BRONZE] {} registros carregados", len(df))

        # Adição de Metadados técnicos
        df["_ingestion_timestamp"] = datetime.now(timezone.utc)
        df["_source"] = "kaggle"

        logger.info("[BRONZE] Salvando arquivo Parquet em: {}", BRONZE_FILE)

        df.to_parquet(
            BRONZE_FILE,
            engine="pyarrow",
            index=False,
        )

        logger.success("[BRONZE] Camada Bronze criada com sucesso")

    except Exception:
        logger.exception("[BRONZE] Erro crítico ao gerar camada Bronze")
        raise
