import os
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
from src.utils.logger import logger

BASE_DATA_DIR = Path(os.getenv("AIRFLOW_DATA_DIR", "data"))

BRONZE_FILE = BASE_DATA_DIR / "bronze/movies_raw.parquet"
SILVER_FILE = BASE_DATA_DIR / "silver/movies_clean.parquet"


def normalize_genres(value: str | None) -> str:
    """
    Padroniza a coluna de gêneros removendo espaços extras.
    """
    if pd.isna(value) or value == "":
        return "Unknown"

    genres = [genre.strip() for genre in str(value).split(",")]
    return ",".join(genres)


def create_silver_layer(force_refresh: bool = False, **kwargs) -> None:
    """
    Cria a camada Silver: limpeza, padronização e validação de dados.
    """
    try:
        logger.info("[SILVER] Iniciando processamento da camada Silver")

        # Garantir que o diretório de destino exista
        SILVER_FILE.parent.mkdir(parents=True, exist_ok=True)

        if not BRONZE_FILE.exists():
            raise FileNotFoundError(f"Arquivo Bronze não encontrado em: {BRONZE_FILE}")

        # Idempotência
        if SILVER_FILE.exists() and not force_refresh:
            logger.info(
                "[SILVER] Arquivo já existe em {}. Pulando processamento.", SILVER_FILE
            )
            return

        logger.info("[SILVER] Lendo arquivo Bronze: {}", BRONZE_FILE)
        df = pd.read_parquet(BRONZE_FILE)
        initial_count = len(df)
        logger.info("[SILVER] {} registros carregados da camada Bronze", initial_count)

        # 1. Limpeza básica
        df = df[df["imdb_id"].notna()]
        df = df.drop_duplicates(subset=["imdb_id"])

        # 2. Padronização
        df["genres"] = df["genres"].apply(normalize_genres)

        # 3. Conversão de tipos
        df["year"] = df["year"].astype("Int64")
        df["runtime_minutes"] = df["runtime_minutes"].astype("Int64")
        df["num_votes"] = df["num_votes"].astype("Int64")
        df["average_rating"] = df["average_rating"].astype(float)

        # 4. Validações de negócio
        df = df[df["year"].between(1980, 2026)]
        df = df[df["average_rating"].between(0, 10)]
        df = df[df["imdb_url"].str.startswith("https://www.imdb.com/title/", na=False)]

        final_count = len(df)
        logger.info(
            "[SILVER] Registros removidos após limpeza: {}", initial_count - final_count
        )

        # 5. Metadados de processamento
        df["_silver_timestamp"] = datetime.now(timezone.utc)

        logger.info("[SILVER] Salvando arquivo Parquet em: {}", SILVER_FILE)
        df.to_parquet(SILVER_FILE, engine="pyarrow", index=False)

        logger.success(
            "[SILVER] Camada Silver criada com sucesso. Total final: {}", final_count
        )

    except Exception:
        logger.exception("[SILVER] Erro crítico ao processar camada Silver")
        raise
