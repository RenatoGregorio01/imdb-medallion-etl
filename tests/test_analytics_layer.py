from src.transform.analytics import (
    GENRE_STATS_FILE,
    YEARLY_STATS_FILE,
    create_analytics_layer,
)


def test_create_analytics_layer() -> None:

    create_analytics_layer(
        force_refresh=True
    )

    assert GENRE_STATS_FILE.exists()

    assert YEARLY_STATS_FILE.exists()


def test_create_analytics_layer_idempotent() -> None:

    create_analytics_layer()

    assert GENRE_STATS_FILE.exists()
    