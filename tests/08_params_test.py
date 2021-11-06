import pytest


def test_parameterization(letter):
    print(f"\n   Running test_parameterization with {letter}")


def test_modes(mode):
    print(f"\n   Running test_modes with {mode}")


@pytest.fixture(params=["a", "b", "c", "d", "e"])
def letter(request):
    """
    Fixtures with parameters will run once per param
    (You can access the current param via the request fixture)
    """
    yield request.param


@pytest.fixture(params=[1, 2, 3], ids=['foo', 'bar', 'baz'])
def mode(request):
    """
    Fixtures with parameters will run once per param
    (You can access the current param via the request fixture)
    """
    yield request.param
