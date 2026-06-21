import os
from pathlib import Path
from src.utils.logger import logger
from src.utils.oci_utils import upload_to_oci

DATASET = "elvisbui/imdb-top-movies-1980-2026"
RAW_PATH = Path("data/raw")
FILE_NAME = "imdb_top_movies_1980_2026.csv"

def download_dataset() -> None:
    try:
        RAW_PATH.mkdir(parents=True, exist_ok=True)
        csv_file = RAW_PATH / FILE_NAME

        if not csv_file.exists():
            logger.info("[EXTRACT] Autenticando e baixando dataset do Kaggle: {}", DATASET)
            
            from kaggle.api.kaggle_api_extended import KaggleApi
            api = KaggleApi()
            api.authenticate()
            
            api.dataset_download_files(DATASET, path=RAW_PATH, unzip=True)
            logger.success("[EXTRACT] Download concluído com sucesso")
        else:
            logger.info("[EXTRACT] Dataset já existe localmente")

        # --- INTEGRAÇÃO OCI ---
        if os.getenv("GITHUB_ACTIONS") != "true":
            logger.info("[EXTRACT] Iniciando backup da camada Bronze na OCI")
            upload_to_oci(file_path=str(csv_file), object_name=f"bronze/{FILE_NAME}")
        else:
            logger.info("[EXTRACT] Ambiente CI: Pulando upload para OCI.")

    except Exception:
        logger.exception("[EXTRACT] Erro no fluxo de extração")
        raise

if __name__ == "__main__":
    download_dataset()
