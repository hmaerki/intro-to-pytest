"""
pytest --collect-only -m smoke

See the output to verify which tests have been selected for
a smoke test.

Demonstrate different way on how to use a smoke parameter.
"""
import logging
from typing import List, Callable, Any, Tuple, Iterator, Union
from collections import abc

import pytest

logger = logging.getLogger(__file__)


def _pytest_param_wrapper(param, marks, identifier=None):
    def is_iterable(param: Any) -> bool:
        """
        This is somehow the counterpart to
        https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
        """
        if isinstance(param, abc.Iterable):
            if isinstance(param, str):
                return False
            return True
        return False

    if is_iterable(param):
        return pytest.param(*param, marks=marks, id=identifier)
    return pytest.param(param, marks=marks, id=identifier)


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
        yield _pytest_param_wrapper(param, marks=marks)


def add_smoke_by_values(
    params: list,
    smoke_params: Union[List, Tuple],
) -> Iterator[Any]:
    """
    This functions adds the smoke parameter to the 'params' in 'smoke_params'.
    """
    assert isinstance(smoke_params, (list, tuple))

    smoke_params = smoke_params.copy()

    for param in params:
        try:
            smoke_params.remove(param)
            yield _pytest_param_wrapper(param, marks=pytest.mark.smoke)
        except ValueError:
            yield _pytest_param_wrapper(param, marks=())

    if len(smoke_params) > 0:
        err = f"These 'smoke_params' have been provided {sorted(smoke_params)!r} but are not in the list of the given test parameters {params!r}!"
        raise AttributeError(err)


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
            yield _pytest_param_wrapper(
                param,
                marks=pytest.mark.smoke if smoke else (),
            )
        return

    if callback_with_id is not None:
        for param in params:
            smoke, identifier = callback_with_id(param)
            assert isinstance(smoke, bool)
            assert isinstance(identifier, str)
            yield _pytest_param_wrapper(
                param,
                marks=pytest.mark.smoke if smoke else (),
                identifier=identifier,
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
    identifier = f"{param}"
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
    "number",
    add_smoke_by_callback([1, 2, 3, 4, 5], callback_with_id=get_smoke_with_id),
)
def test_numbers_8(number):
    print(f"\n   Running test_parameterization with {number}")


@pytest.mark.parametrize(
    "x, y",
    add_smoke_by_index([(1, 2), (3, 4), (5, 6)], list_smoke_idx=(0, -1)),
)
def test_letters_9(x: int, y: int):
    print(f"\n   Running test_parameterization with x={x}, y={y}")


@pytest.mark.parametrize(
    "x, y",
    add_smoke_by_values([(1, 2), (3, 4), (5, 6)], smoke_params=[(3, 4)]),
)
def test_letters_9(x: int, y: int):
    print(f"\n   Running test_parameterization with x={x}, y={y}")
