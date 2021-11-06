import pytest


def test_with_introspection(introspective_fixture):
    print("\nRunning test_with_introspection...")
    assert True


@pytest.fixture
def introspective_fixture(request):
    """
    The request fixture allows introspection into the
    "requesting" test case
    """
    print("\n\nintrospective_fixture:")
    print(f"...Called at {request.scope}-level scope")
    print(f"   ...In the {request.module} module")
    print(f"      ...On the {request.node} node")
