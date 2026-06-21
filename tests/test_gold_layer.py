from src.transform.gold import GOLD_FILES, create_gold_layer


def test_create_gold_layer() -> None:
    create_gold_layer(force_refresh=True)

    assert GOLD_FILES["dim_movie.parquet"].exists()
    assert GOLD_FILES["dim_genre.parquet"].exists()
    assert GOLD_FILES["fact_movie.parquet"].exists()
    assert GOLD_FILES["bridge_movie_genre.parquet"].exists()


def test_create_gold_layer_idempotent() -> None:
    create_gold_layer()

    # Verifica se pelo menos o arquivo principal foi criado
    assert GOLD_FILES["dim_movie.parquet"].exists()
