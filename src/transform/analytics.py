import os
from pathlib import Path
import duckdb
from src.utils.logger import logger
from src.utils.oci_utils import upload_to_oci

BASE_DATA_DIR = Path(os.getenv("AIRFLOW_DATA_DIR", "data"))
GOLD_PATH = BASE_DATA_DIR / "gold"
ANALYTICS_PATH = GOLD_PATH / "analytics"

ANALYTICS_FILES = {
    "genre_statistics.parquet": ANALYTICS_PATH / "genre_statistics.parquet",
    "yearly_movie_statistics.parquet": ANALYTICS_PATH
    / "yearly_movie_statistics.parquet",
}


def create_analytics_layer(force_refresh: bool = False, **kwargs) -> None:
    """
    Gera tabelas agregadas via DuckDB e sincroniza os resultados com a OCI.
    """
    try:
        logger.info("[ANALYTICS] Iniciando processamento da camada analítica")
        ANALYTICS_PATH.mkdir(parents=True, exist_ok=True)

        # Processamento (Idempotência)
        if force_refresh or not all(p.exists() for p in ANALYTICS_FILES.values()):
            conn = duckdb.connect(database=":memory:")

            logger.info("[ANALYTICS] Gerando estatísticas por gênero")
            conn.execute(f"""
                COPY (
                    SELECT g.genre_name, COUNT(*) AS movie_count, ROUND(AVG(f.average_rating), 2) AS avg_rating, SUM(f.num_votes) AS total_votes
                    FROM read_parquet('{GOLD_PATH}/fact_movie.parquet') f
                    JOIN read_parquet('{GOLD_PATH}/bridge_movie_genre.parquet') b ON f.movie_key = b.movie_key
                    JOIN read_parquet('{GOLD_PATH}/dim_genre.parquet') g ON b.genre_key = g.genre_key
                    GROUP BY g.genre_name ORDER BY avg_rating DESC
                ) TO '{ANALYTICS_FILES['genre_statistics.parquet']}' (FORMAT PARQUET)
            """)

            logger.info("[ANALYTICS] Gerando estatísticas por ano")
            conn.execute(f"""
                COPY (
                    SELECT d.year, COUNT(*) AS movie_count, ROUND(AVG(f.average_rating), 2) AS avg_rating, ROUND(AVG(d.runtime_minutes), 2) AS avg_runtime, SUM(f.num_votes) AS total_votes
                    FROM read_parquet('{GOLD_PATH}/dim_movie.parquet') d
                    JOIN read_parquet('{GOLD_PATH}/fact_movie.parquet') f ON d.movie_key = f.movie_key
                    GROUP BY d.year ORDER BY d.year
                ) TO '{ANALYTICS_FILES['yearly_movie_statistics.parquet']}' (FORMAT PARQUET)
            """)
            conn.close()
            logger.success("[ANALYTICS] Arquivos gerados localmente")
        else:
            logger.info("[ANALYTICS] Arquivos já existem. Pulando processamento local.")

        # --- INTEGRAÇÃO OCI ---
        logger.info("[ANALYTICS] Sincronizando camada analítica com a OCI")
        for filename, filepath in ANALYTICS_FILES.items():
            upload_to_oci(file_path=str(filepath), object_name=f"analytics/{filename}")

    except Exception:
        logger.exception("[ANALYTICS] Falha ao processar camada analítica")
        raise


if __name__ == "__main__":
    create_analytics_layer()
