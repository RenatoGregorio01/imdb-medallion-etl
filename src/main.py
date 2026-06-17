from src.extract.download_dataset import download_dataset
from src.transform.bronze import create_bronze_layer
from src.transform.silver import create_silver_layer
from src.transform.gold import create_gold_layer
from src.transform.analytics import create_analytics_layer


def main() -> None:
    download_dataset()
    create_bronze_layer()
    create_silver_layer()
    create_gold_layer(force_refresh=True)
    create_analytics_layer(force_refresh=True)


if __name__ == "__main__":
    main()
    