from src.transform.silver import (
    normalize_genres,
)


def test_normalize_genres() -> None:

    assert (
        normalize_genres(
            "Action, Drama"
        )
        == "Action,Drama"
    )


def test_normalize_genres_extra_spaces() -> None:

    assert (
        normalize_genres(
            "Action , Drama"
        )
        == "Action,Drama"
    )


def test_normalize_genres_null() -> None:

    assert (
        normalize_genres(None)
        == "Unknown"
    )
    