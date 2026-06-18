from unittest.mock import patch

from src.main import main


@patch("src.main.create_analytics_layer")
@patch("src.main.create_gold_layer")
@patch("src.main.create_silver_layer")
@patch("src.main.create_bronze_layer")
@patch("src.main.download_dataset")
def test_main_pipeline(
    mock_download,
    mock_bronze,
    mock_silver,
    mock_gold,
    mock_analytics,
) -> None:

    main()

    mock_download.assert_called_once()

    mock_bronze.assert_called_once()

    mock_silver.assert_called_once()

    mock_gold.assert_called_once_with(
        force_refresh=True
    )

    mock_analytics.assert_called_once_with(
        force_refresh=True
    )
    