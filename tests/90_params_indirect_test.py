import pytest


PROFILE_TEST_CABLING_LST = ("out a -> in 1", "out a -> in 2")


@pytest.fixture
def indirect_fixture(request) -> None:
    test_cabling = request.param
    yield f"Modified by indirect_fixture: {test_cabling}"


@pytest.mark.parametrize("indirect_fixture", PROFILE_TEST_CABLING_LST, indirect=True)
def test_marker_indirect(indirect_fixture):
    test_cabling = indirect_fixture
    print(f"Test {test_cabling}")


@pytest.mark.parametrize("indirect_fixture", PROFILE_TEST_CABLING_LST)
def test_marker_direct(indirect_fixture):
    test_cabling = indirect_fixture
    print(f"Test {test_cabling}")
