from src.extract.download_dataset import download_dataset
from src.transform.bronze import create_bronze_layer


def main() -> None:
    download_dataset()
    create_bronze_layer()


if __name__ == "__main__":
    main()
    