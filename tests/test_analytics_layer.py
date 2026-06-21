from src.transform.analytics import ANALYTICS_FILES, create_analytics_layer


def test_create_analytics_layer() -> None:
    """
    Testa a criação da camada Analytics forçando a atualização dos arquivos.
    """
    create_analytics_layer(force_refresh=True)

    # Verifica se os arquivos foram criados usando as chaves do dicionário
    assert ANALYTICS_FILES["genre_statistics.parquet"].exists()
    assert ANALYTICS_FILES["yearly_movie_statistics.parquet"].exists()


def test_create_analytics_layer_idempotent() -> None:
    """
    Testa a idempotência da camada Analytics.
    """
    create_analytics_layer()

    # Verifica se o arquivo principal existe após a execução
    assert ANALYTICS_FILES["genre_statistics.parquet"].exists()
