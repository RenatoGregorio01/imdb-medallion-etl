import os
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
from src.utils.logger import logger
from src.utils.oci_utils import upload_to_oci 

BASE_DATA_DIR = Path(os.getenv("AIRFLOW_DATA_DIR", "data"))
RAW_FILE = BASE_DATA_DIR / "raw/imdb_top_movies_1980_2026.csv"
BRONZE_FILE = BASE_DATA_DIR / "bronze/movies_raw.parquet"


def create_bronze_layer(force_refresh: bool = False, **kwargs) -> None:
    """
    Cria a camada Bronze transformando o CSV de origem em Parquet e faz upload para OCI.
    """
    try:
        logger.info("[BRONZE] Iniciando geração da camada Bronze")

        BRONZE_FILE.parent.mkdir(parents=True, exist_ok=True)

        if not RAW_FILE.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {RAW_FILE}")

        if BRONZE_FILE.exists() and not force_refresh:
            logger.info("[BRONZE] Arquivo já existe. Pulando processamento.")
        else:
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

            df["_ingestion_timestamp"] = datetime.now(timezone.utc)
            df["_source"] = "kaggle"

            logger.info("[BRONZE] Salvando arquivo Parquet em: {}", BRONZE_FILE)
            df.to_parquet(BRONZE_FILE, engine="pyarrow", index=False)
            logger.success("[BRONZE] Camada Bronze criada com sucesso")

        # --- INTEGRAÇÃO OCI ---
        logger.info("[BRONZE] Enviando arquivo para a camada Bronze na OCI")
        upload_to_oci(
            file_path=str(BRONZE_FILE),
            object_name=f"bronze/{BRONZE_FILE.name}"
        )

    except Exception:
        logger.exception("[BRONZE] Erro crítico ao gerar camada Bronze")
        raise


if __name__ == "__main__":
    create_bronze_layer()
