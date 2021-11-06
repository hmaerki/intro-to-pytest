import pytest
from pytest_dependency import DependencyManager

STATE = {}

# COUNT = 5

# @pytest.mark.repeat(3)
# @pytest.mark.parametrize("i", range(COUNT), ids=lambda i: f"{i:03d}-{COUNT:03d}")
@pytest.mark.dependency(name="daq")
def test_a(request, foo_count):
    i, count = foo_count

    assert i != 3
    STATE[request.node.nodeid] = f"Data {i:02d}({count:02d})"


@pytest.mark.dependency(name="result", depends=["daq"])
def test_b(request):
    print()
    for nodeid, data in STATE.items():
        print(f"fnodeid:{nodeid}, data:{data}")

    # manager = DependencyManager.getManager(request.node, scope='package')
    # for nodeid, results in manager.results.items():
    #     if results.isSuccess():
    #         data = STATE[nodeid]
    #         print(f"PASSED fnodeid:{nodeid}, data:{data}")
