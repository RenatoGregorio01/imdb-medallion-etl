from src.transform.silver import (
    SILVER_FILE,
    create_silver_layer,
)


def test_create_silver_layer() -> None:

    create_silver_layer(force_refresh=True)

    assert SILVER_FILE.exists()


def test_create_silver_layer_idempotent() -> None:

    create_silver_layer()

    assert SILVER_FILE.exists()
