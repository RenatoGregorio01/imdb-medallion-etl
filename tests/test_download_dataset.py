from pathlib import Path


def test_raw_directory_exists():
    assert Path("data/raw").exists()

    