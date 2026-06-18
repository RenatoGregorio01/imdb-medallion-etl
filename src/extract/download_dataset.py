from pathlib import Path

from src.utils.logger import logger

DATASET = "elvisbui/imdb-top-movies-1980-2026"
RAW_PATH = Path("data/raw")


def download_dataset() -> None:
    try:
        logger.info(
            "[EXTRACT] Iniciando download do dataset"
        )

        RAW_PATH.mkdir(
            parents=True,
            exist_ok=True
        )

        csv_file = (
            RAW_PATH /
            "imdb_top_movies_1980_2026.csv"
        )

        if csv_file.exists():
            logger.info(
                "[EXTRACT] Dataset já existe: {}",
                csv_file
            )
            return

        logger.info(
            "[EXTRACT] Importando cliente Kaggle"
        )

        from kaggle.api.kaggle_api_extended import (
            KaggleApi,
        )

        logger.info(
            "[EXTRACT] Autenticando na API do Kaggle"
        )

        api = KaggleApi()
        api.authenticate()

        logger.info(
            "[EXTRACT] Baixando dataset: {}",
            DATASET
        )

        api.dataset_download_files(
            DATASET,
            path=RAW_PATH,
            unzip=True,
        )

        logger.success(
            "[EXTRACT] Download concluído com sucesso"
        )

    except Exception:
        logger.exception(
            "[EXTRACT] Erro ao realizar download do dataset"
        )
        raise


if __name__ == "__main__":
    download_dataset()
    