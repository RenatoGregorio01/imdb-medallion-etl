import os
from pathlib import Path
import pandas as pd
from src.utils.logger import logger
from src.utils.oci_utils import upload_to_oci 


BASE_DATA_DIR = Path(os.getenv("AIRFLOW_DATA_DIR", "data"))
SILVER_FILE = BASE_DATA_DIR / "silver/movies_clean.parquet"
GOLD_PATH = BASE_DATA_DIR / "gold"


GOLD_FILES = {
    "dim_movie.parquet": GOLD_PATH / "dim_movie.parquet",
    "dim_genre.parquet": GOLD_PATH / "dim_genre.parquet",
    "bridge_movie_genre.parquet": GOLD_PATH / "bridge_movie_genre.parquet",
    "fact_movie.parquet": GOLD_PATH / "fact_movie.parquet",
}

def create_dim_movie(df: pd.DataFrame) -> pd.DataFrame:
    dim_movie = df[
        ["imdb_id", "title", "original_title", "year", "runtime_minutes", "imdb_url"]
    ].copy()
    dim_movie.insert(0, "movie_key", range(1, len(dim_movie) + 1))
    return dim_movie

def create_dim_genre(df: pd.DataFrame) -> pd.DataFrame:
    genres = df["genres"].str.split(",").explode().str.strip().dropna().unique()
    dim_genre = pd.DataFrame({"genre_name": sorted(genres)})
    dim_genre.insert(0, "genre_key", range(1, len(dim_genre) + 1))
    return dim_genre

def create_fact_movie(df: pd.DataFrame, dim_movie: pd.DataFrame) -> pd.DataFrame:
    fact_movie = df[["average_rating", "num_votes"]].copy()
    fact_movie.insert(0, "movie_key", dim_movie["movie_key"])
    return fact_movie

def create_bridge_movie_genre(df: pd.DataFrame, dim_movie: pd.DataFrame, dim_genre: pd.DataFrame) -> pd.DataFrame:
    genre_lookup = dict(zip(dim_genre["genre_name"], dim_genre["genre_key"], strict=False))
    bridge_rows = []
    for movie_key, genres in zip(dim_movie["movie_key"], df["genres"], strict=False):
        for genre in str(genres).split(","):
            genre_stripped = genre.strip()
            if genre_stripped in genre_lookup:
                bridge_rows.append({"movie_key": movie_key, "genre_key": genre_lookup[genre_stripped]})
    return pd.DataFrame(bridge_rows)

def create_gold_layer(force_refresh: bool = False, **kwargs) -> None:
    """
    Cria a camada Gold (Star Schema) e sincroniza cada arquivo com a OCI.
    """
    try:
        logger.info("[GOLD] Iniciando geração da camada Gold")
        GOLD_PATH.mkdir(parents=True, exist_ok=True)

        if not SILVER_FILE.exists():
            raise FileNotFoundError(f"Arquivo Silver não encontrado: {SILVER_FILE}")

        # Processamento
        if force_refresh or not all(p.exists() for p in GOLD_FILES.values()):
            df = pd.read_parquet(SILVER_FILE)
            
            logger.info("[GOLD] Criando modelos dimensionais")
            dim_movie = create_dim_movie(df)
            dim_genre = create_dim_genre(df)
            fact_movie = create_fact_movie(df, dim_movie)
            bridge_movie_genre = create_bridge_movie_genre(df, dim_movie, dim_genre)

            dim_movie.to_parquet(GOLD_FILES["dim_movie.parquet"], index=False)
            dim_genre.to_parquet(GOLD_FILES["dim_genre.parquet"], index=False)
            fact_movie.to_parquet(GOLD_FILES["fact_movie.parquet"], index=False)
            bridge_movie_genre.to_parquet(GOLD_FILES["bridge_movie_genre.parquet"], index=False)
            logger.success("[GOLD] Arquivos salvos localmente")
        else:
            logger.info("[GOLD] Arquivos já existem. Pulando processamento.")

        # --- INTEGRAÇÃO OCI ---
        logger.info("[GOLD] Iniciando sincronização da camada Gold com a OCI")
        for filename, filepath in GOLD_FILES.items():
            upload_to_oci(
                file_path=str(filepath),
                object_name=f"gold/{filename}"
            )

    except Exception:
        logger.exception("[GOLD] Erro crítico na camada Gold")
        raise
