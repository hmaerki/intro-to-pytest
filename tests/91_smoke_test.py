"""
pytest --collect-only -m smoke

See the output to verify which tests have been selected for
a smoke test.

Demonstrate different way on how to use a smoke parameter.
"""
import pytest


@pytest.mark.parametrize("letter", ["a", "b", "c", "d", "e"])
def test_letters_1(letter):
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
def test_letters_2(letter):
    print(f"\n   Running test_parameterization with {letter}")


@pytest.mark.smoke
@pytest.mark.parametrize(
    "letter",
    ["a", "b", "c", "d", "e"],
)
def test_letters_3(letter):
    print(f"\n   Running test_parameterization with {letter}")


def fumigate(params: list, first=True, last=False) -> list:
    '''
    This functions adds the smoke paramter to first/last element.
    '''
    set_index = set()
    if first:
        set_index.add(0)
    if last:
        set_index.add(len(params)-1)

    def inner():
        for i, param in enumerate(params):
            if i in set_index:
                yield pytest.param(param, marks=pytest.mark.smoke)
                continue
            yield param

    return inner()

@pytest.mark.parametrize(
    "letter",
    fumigate(["a", "b", "c", "d", "e"], first=True, last=True),
)
def test_letters_4(letter):
    print(f"\n   Running test_parameterization with {letter}")
