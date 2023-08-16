"""
pytest --collect-only -m smoke

See the output to verify which tests have been selected for
a smoke test.

Demonstrate different way on how to use a smoke parameter.
"""
from typing import List, Callable, Any, Tuple, Iterator
import pytest


def add_smoke_by_index(params: list, list_smoke_idx: List[int] = None) -> Iterator[Any]:
    """
    This functions adds the smoke parameter to selected tests.
    `text_idx` is an element of `list_smoke_idx`.
    test_idx >= 0: Add smoke to 'params[test_idx]'.
    test_idx < 0: Add smoke to 'params[test_idx-len]'.
    """

    size = len(params)
    for i, param in enumerate(params):
        marks = ()
        if i in list_smoke_idx:
            marks = pytest.mark.smoke
        i_reverse = i - size
        if i_reverse in list_smoke_idx:
            marks = pytest.mark.smoke
        yield pytest.param(*param, marks=marks)


def add_smoke_by_callback(
    params: list,
    callback: Callable[[Any], bool] = None,
    callback_with_id: Callable[[Any], Tuple[bool, str]] = None,
) -> Iterator[Any]:
    """
    'callback'. This expects a callback 'def get_smoke(param): return True'. If the callback returns True, the test will be marked as smoke.
    'callback_with_id'. This expects a callback 'def get_smoke_and_id(param): return (True, "theid")'. As above, but also the id may be returned.
    """

    if callback is not None:
        for param in params:
            smoke = callback(param)
            yield pytest.param(
                *param,
                marks=pytest.mark.smoke if smoke else (),
            )
        return

    if callback_with_id is not None:
        for param in params:
            smoke, identifier = callback_with_id(param)
            yield pytest.param(
                *param,
                marks=pytest.mark.smoke if smoke else (),
                id=identifier,
            )
        return

    raise AttributeError(
        "Exactly one of 'callback' or 'callback_with_id' must be provied!"
    )


@pytest.mark.parametrize("letter", ["a", "b", "c"])
def test_letters_1(letter):
    print(f"\n   Running test_parameterization with {letter}")


@pytest.mark.smoke
@pytest.mark.parametrize(
    "letter",
    ["a", "b", "c"],
)
def test_letters_2(letter):
    print(f"\n   Running test_parameterization with {letter}")


@pytest.mark.parametrize(
    "letter",
    [
        "a",
        "b",
        "c",
        pytest.param("d", marks=pytest.mark.smoke),
        "e",
    ],
)
def test_letters_3(letter):
    print(f"\n   Running test_parameterization with {letter}")


@pytest.mark.parametrize(
    "letter",
    add_smoke_by_index(["a", "b", "c"], list_smoke_idx=(0, -1)),
)
def test_letters_4(letter):
    print(f"\n   Running test_parameterization with {letter}")


@pytest.mark.parametrize(
    "letter",
    add_smoke_by_index(["a", "b", "c", "d", "e"], list_smoke_idx=(1, -2, -1)),
)
def test_letters_5(letter):
    print(f"\n   Running test_parameterization with {letter}")


@pytest.mark.parametrize(
    "letter",
    add_smoke_by_callback(
        ["a", "b", "c", "d", "e"], callback=lambda p: p in ("b", "d")
    ),
)
def test_letters_6(letter):
    print(f"\n   Running test_parameterization with {letter}")


def get_smoke_with_id(param: str) -> Tuple[bool, str]:
    smoke = param in ("b", "d")
    identifier = param
    if smoke:
        identifier += "(smoke)"
    return smoke, identifier


@pytest.mark.parametrize(
    "letter",
    add_smoke_by_callback(
        ["a", "b", "c", "d", "e"], callback_with_id=get_smoke_with_id
    ),
)
def test_letters_7(letter):
    print(f"\n   Running test_parameterization with {letter}")

@pytest.mark.parametrize(
    "x, y",
    add_smoke_by_index(
        [(1, 2), (3, 4), (5, 6)], list_smoke_idx=(0, -1)
    ),
)
def test_letters_8(x, y):
    print(f"\n   Running test_parameterization with x={x}, y={y}")
