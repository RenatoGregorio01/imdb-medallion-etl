from pathlib import Path

from src.transform.bronze import (
    BRONZE_FILE,
    create_bronze_layer,
)


def test_create_bronze_layer() -> None:

    create_bronze_layer(force_refresh=True)

    assert BRONZE_FILE.exists()


def test_create_bronze_layer_idempotent() -> None:

    create_bronze_layer()

    assert Path(BRONZE_FILE).exists()
