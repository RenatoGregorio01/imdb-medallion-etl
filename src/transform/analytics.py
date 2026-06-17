from pathlib import Path

import duckdb

from src.utils.logger import logger

GOLD_PATH = Path("data/gold")

ANALYTICS_PATH = Path(
    "data/gold/analytics"
)

GENRE_STATS_FILE = (
    ANALYTICS_PATH /
    "genre_statistics.parquet"
)

YEARLY_STATS_FILE = (
    ANALYTICS_PATH /
    "yearly_movie_statistics.parquet"
)


def create_analytics_layer(
    force_refresh: bool = False,
) -> None:

    try:

        logger.info(
            "[ANALYTICS] Iniciando camada analítica"
        )

        if (
            GENRE_STATS_FILE.exists()
            and YEARLY_STATS_FILE.exists()
            and not force_refresh
        ):
            logger.info(
                "[ANALYTICS] Arquivos já existem"
            )
            return

        ANALYTICS_PATH.mkdir(
            parents=True,
            exist_ok=True,
        )

        conn = duckdb.connect()

        logger.info(
            "[ANALYTICS] Gerando genre_statistics"
        )

        conn.execute(
            f"""
            COPY (

                SELECT
                    g.genre_name,
                    COUNT(*) AS movie_count,

                    ROUND(
                        AVG(
                            f.average_rating
                        ),
                        2
                    ) AS avg_rating,

                    SUM(
                        f.num_votes
                    ) AS total_votes

                FROM read_parquet(
                    '{GOLD_PATH}/fact_movie.parquet'
                ) f

                JOIN read_parquet(
                    '{GOLD_PATH}/bridge_movie_genre.parquet'
                ) b
                    ON f.movie_key =
                       b.movie_key

                JOIN read_parquet(
                    '{GOLD_PATH}/dim_genre.parquet'
                ) g
                    ON b.genre_key =
                       g.genre_key

                GROUP BY
                    g.genre_name

                ORDER BY
                    avg_rating DESC

            )

            TO '{GENRE_STATS_FILE}'
            (
                FORMAT PARQUET
            )
            """
        )

        logger.info(
            "[ANALYTICS] Gerando yearly_movie_statistics"
        )

        conn.execute(
            f"""
            COPY (

                SELECT
                    d.year,

                    COUNT(*) AS movie_count,

                    ROUND(
                        AVG(
                            f.average_rating
                        ),
                        2
                    ) AS avg_rating,

                    ROUND(
                        AVG(
                            d.runtime_minutes
                        ),
                        2
                    ) AS avg_runtime,

                    SUM(
                        f.num_votes
                    ) AS total_votes

                FROM read_parquet(
                    '{GOLD_PATH}/dim_movie.parquet'
                ) d

                JOIN read_parquet(
                    '{GOLD_PATH}/fact_movie.parquet'
                ) f
                    ON d.movie_key =
                       f.movie_key

                GROUP BY
                    d.year

                ORDER BY
                    d.year

            )

            TO '{YEARLY_STATS_FILE}'
            (
                FORMAT PARQUET
            )
            """
        )

        conn.close()

        logger.success(
            "[ANALYTICS] Camada analítica criada com sucesso"
        )

    except Exception:
        logger.exception(
            "[ANALYTICS] Erro na camada analítica"
        )
        raise
    