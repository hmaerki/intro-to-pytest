from dataclasses import dataclass
import pytest


@dataclass
class Repeat:
    i: int
    count: int

    @property
    def __name__(self):
        return f"{self.i:001d}-{self.count:001d}"

def repeat(count = 3) -> int:
    for i in range(count):
        yield Repeat(i=i, count=count)

@pytest.mark.parametrize("r", repeat(count=4))
def test_repeat_homemade_a(r):
    print(f"{r.i}-{r.count}")
    assert True

@pytest.mark.parametrize("i", range(4), ids=lambda i: f"{i:02d}")
def test_repeat_homemade_b(i):
    assert True
