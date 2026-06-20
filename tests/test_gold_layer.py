from src.transform.gold import (
    BRIDGE_FILE,
    DIM_GENRE_FILE,
    DIM_MOVIE_FILE,
    FACT_MOVIE_FILE,
    create_gold_layer,
)


def test_create_gold_layer() -> None:

    create_gold_layer(force_refresh=True)

    assert DIM_MOVIE_FILE.exists()

    assert DIM_GENRE_FILE.exists()

    assert FACT_MOVIE_FILE.exists()

    assert BRIDGE_FILE.exists()


def test_create_gold_layer_idempotent() -> None:

    create_gold_layer()

    assert DIM_MOVIE_FILE.exists()
