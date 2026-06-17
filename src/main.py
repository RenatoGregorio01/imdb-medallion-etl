from src.extract.download_dataset import download_dataset
from src.transform.bronze import create_bronze_layer
from src.transform.silver import create_silver_layer


def main() -> None:
    download_dataset()
    create_bronze_layer()
    create_silver_layer()


if __name__ == "__main__":
    main()
    