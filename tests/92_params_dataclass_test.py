"""
`tests/08_params_test.py` shows how to write parametrized tests.


This examples demonstrates how to write parametrized tests using dataclasses.
Benefits are:
* Type safety.
* Ease to add/remove parameters.
* Ease to control the id (in pytest displayed within [])
* May be used in standalone tests without pytest.
"""
from dataclasses import dataclass
import pytest


@dataclass
class ParameterX:
    """
    Our test parameters are just objects of this class.
    With this class we may control it's name.
    The use of the class is typesafe - the pytest-approach is not typesafe!
    """

    a: int
    b: int
    expected_result: int
    identifier_note: str = None

    @property
    def identifier(self) -> str:
        """
        This will be the paramter [...] used by pytest.
        """
        ident = f"{self.a}-{self.b}"
        if self.identifier_note is not None:
            ident += self.identifier_note
        return ident


parameters_x = [
    ParameterX(
        a=3,
        b=3,
        expected_result=9,
    ),
    pytest.param(
        ParameterX(
            a=1,
            b=32,
            expected_result=32,
            identifier_note="-very-special-testcase",
        ),
        marks=pytest.mark.smoke,
    ),
    ParameterX(
        a=2,
        b=2,
        expected_result=4,
    ),
]


@pytest.mark.parametrize(
    "param_x",
    parameters_x,
    ids=lambda t: t.identifier,
)
def test_x(param_x: ParameterX):
    assert param_x.a * param_x.b == param_x.expected_result
