from pathlib import Path
from unittest.mock import patch

import pytest

from src.transform.bronze import (
    create_bronze_layer,
)


@patch(
    "src.transform.bronze.RAW_FILE",
    Path("arquivo_inexistente.csv"),
)
def test_bronze_file_not_found() -> None:

    with pytest.raises(
        FileNotFoundError
    ):
        create_bronze_layer(
            force_refresh=True
        )
        