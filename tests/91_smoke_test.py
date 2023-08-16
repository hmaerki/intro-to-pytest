"""
pytest --collect-only -m smoke

See the output to verify which tests have been selected for
a smoke test.

Demonstrate different way on how to use a smoke parameter.
"""
from typing import List
import pytest


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


def add_smoke(params: list, test_idx: List[int] = None) -> list:
    """
    This functions adds the smoke parameter to selected tests.
    test_idx >= 0: Add smoke to 'params[test_idx]'.
    test_idx < 0: Add smoke to 'params[test_idx-len]'.
    """

    def inner():
        size = len(params)
        for i, param in enumerate(params):
            marks = ()
            if i in test_idx:
                marks = pytest.mark.smoke
            i_reverse = i - size
            if i_reverse in test_idx:
                marks = pytest.mark.smoke
            yield pytest.param(param, marks=marks)

    return list(inner())


@pytest.mark.parametrize(
    "letter",
    add_smoke(["a", "b", "c"], test_idx=(0, -1)),
)
def test_letters_4(letter):
    print(f"\n   Running test_parameterization with {letter}")


@pytest.mark.parametrize(
    "letter",
    add_smoke(["a", "b", "c", "d", "e"], test_idx=(1, -2)),
)
def test_letters_5(letter):
    print(f"\n   Running test_parameterization with {letter}")
