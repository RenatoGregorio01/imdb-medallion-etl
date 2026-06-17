from pathlib import Path

import pandas as pd

from src.utils.logger import logger

SILVER_FILE = Path(
    "data/silver/movies_clean.parquet"
)

GOLD_PATH = Path(
    "data/gold"
)

DIM_MOVIE_FILE = (
    GOLD_PATH / "dim_movie.parquet"
)

DIM_GENRE_FILE = (
    GOLD_PATH / "dim_genre.parquet"
)

BRIDGE_FILE = (
    GOLD_PATH / "bridge_movie_genre.parquet"
)

FACT_MOVIE_FILE = (
    GOLD_PATH / "fact_movie.parquet"
)


def create_dim_movie(
    df: pd.DataFrame,
) -> pd.DataFrame:
    dim_movie = df[
        [
            "imdb_id",
            "title",
            "original_title",
            "year",
            "runtime_minutes",
            "imdb_url",
        ]
    ].copy()

    dim_movie.insert(
        0,
        "movie_key",
        range(1, len(dim_movie) + 1),
    )

    return dim_movie


def create_dim_genre(
    df: pd.DataFrame,
) -> pd.DataFrame:

    genres = (
        df["genres"]
        .str.split(",")
        .explode()
        .str.strip()
        .dropna()
        .unique()
    )

    dim_genre = pd.DataFrame(
        {
            "genre_name": sorted(genres),
        }
    )

    dim_genre.insert(
        0,
        "genre_key",
        range(1, len(dim_genre) + 1),
    )

    return dim_genre


def create_fact_movie(
    df: pd.DataFrame,
    dim_movie: pd.DataFrame,
) -> pd.DataFrame:

    fact_movie = df[
        [
            "average_rating",
            "num_votes",
        ]
    ].copy()

    fact_movie.insert(
        0,
        "movie_key",
        dim_movie["movie_key"],
    )

    return fact_movie


def create_bridge_movie_genre(
    df: pd.DataFrame,
    dim_movie: pd.DataFrame,
    dim_genre: pd.DataFrame,
) -> pd.DataFrame:

    # Cria mapa: gênero -> chave
    genre_lookup = dict(
        zip(
            dim_genre["genre_name"],
            dim_genre["genre_key"],
            strict=False,
        )
    )

    bridge_rows = []

    # Percorre os filmes usando zip
    for movie_key, genres in zip(
        dim_movie["movie_key"],
        df["genres"],
        strict=False,
    ):

        for genre in str(genres).split(","):

            bridge_rows.append(
                {
                    "movie_key": movie_key,
                    "genre_key": genre_lookup[
                        genre.strip()
                    ],
                }
            )

    return pd.DataFrame(bridge_rows)


def create_gold_layer(
    force_refresh: bool = False,
) -> None:

    try:

        logger.info(
            "[GOLD] Iniciando camada Gold"
        )

        if not SILVER_FILE.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {SILVER_FILE}"
            )

        if (
            DIM_MOVIE_FILE.exists()
            and DIM_GENRE_FILE.exists()
            and BRIDGE_FILE.exists()
            and FACT_MOVIE_FILE.exists()
            and not force_refresh
        ):
            logger.info(
                "[GOLD] Arquivos já existem"
            )
            return

        logger.info(
            "[GOLD] Lendo camada Silver"
        )

        df = pd.read_parquet(
            SILVER_FILE
        )

        logger.info(
            "[GOLD] {} registros carregados",
            len(df),
        )

        GOLD_PATH.mkdir(
            parents=True,
            exist_ok=True,
        )

        logger.info(
            "[GOLD] Criando dim_movie"
        )

        dim_movie = create_dim_movie(
            df
        )

        logger.info(
            "[GOLD] Criando dim_genre"
        )

        dim_genre = create_dim_genre(
            df
        )

        logger.info(
            "[GOLD] Criando fact_movie"
        )

        fact_movie = create_fact_movie(
            df,
            dim_movie,
        )

        logger.info(
            "[GOLD] Criando bridge_movie_genre"
        )

        bridge_movie_genre = (
            create_bridge_movie_genre(
                df,
                dim_movie,
                dim_genre,
            )
        )

        dim_movie.to_parquet(
            DIM_MOVIE_FILE,
            engine="pyarrow",
            index=False,
        )

        dim_genre.to_parquet(
            DIM_GENRE_FILE,
            engine="pyarrow",
            index=False,
        )

        fact_movie.to_parquet(
            FACT_MOVIE_FILE,
            engine="pyarrow",
            index=False,
        )

        bridge_movie_genre.to_parquet(
            BRIDGE_FILE,
            engine="pyarrow",
            index=False,
        )

        logger.success(
            "[GOLD] Camada Gold criada com sucesso"
        )

        logger.info(
            "[GOLD] dim_movie: {} registros",
            len(dim_movie),
        )

        logger.info(
            "[GOLD] dim_genre: {} registros",
            len(dim_genre),
        )

        logger.info(
            "[GOLD] fact_movie: {} registros",
            len(fact_movie),
        )

        logger.info(
            "[GOLD] bridge_movie_genre: {} registros",
            len(bridge_movie_genre),
        )

    except Exception:
        logger.exception(
            "[GOLD] Erro na camada Gold"
        )
        raise