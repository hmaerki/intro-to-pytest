from typing import List
import itertools

from dataclasses import dataclass
import pytest

from tests.utils_parametrize import ParamProtocol, dataclass_param


@dataclass(frozen=True)
class ParameterX(ParamProtocol):
    a: int
    b: int
    expected_result: int
    id_note: str = None
    "This implements 'ParamProtocol'"
    marks: List[pytest.MarkDecorator] | None = None
    "This implements 'ParamProtocol'"

    @property
    def id(self) -> str:
        "This implements 'ParamProtocol'"
        return f"{self.a}-{self.b}"


params_x = [
    ParameterX(
        a=3,
        b=3,
        expected_result=9,
    ),
    ParameterX(
        a=1,
        b=32,
        expected_result=32,
        id_note="run-twice",
        marks=(pytest.mark.slow(2),),
    ),
    ParameterX(
        a=2, b=2, expected_result=4, marks=(pytest.mark.slow(5), pytest.mark.skip)
    ),
    ParameterX(
        a=2,
        b=2,
        expected_result=4,
        marks=(pytest.mark.xfail,),
    ),
]


@dataclass_param(params=params_x)
def test_x(param: ParameterX):
    """
    Positive: Support for typehints for complex parameters.
    Positive: The decorator and test signature are much simpler.
    Positive: The logic for id creation and marks for parameters is moved away in the parameter.
    """
    assert param.a * param.b == param.expected_result


@dataclass(frozen=True)
class ParameterCombined(ParamProtocol):
    channel: int
    x: ParameterX

    @property
    def marks(self) -> List[pytest.MarkDecorator] | None:
        '''
        We may add/remove markers to combined parameters.
        This is not possible using two more 'pytest.mark.param'!
        '''
        if (self.channel == 0) and (self.x.b == 32):
            return (* self.x.marks, pytest.mark.smoke)
        return self.x.marks

    @property
    def id(self) -> str:
        '''
        We may define the id combined parameters.
        This is not possible using two more 'pytest.mark.param'!
        '''
        return f"ch{self.channel}/{self.x.id}"

    @staticmethod
    def product(channels: List[int], list_x: List[ParameterX]) -> List['ParameterCombined']:
        for channel, x in itertools.product(channels, list_x):
            yield ParameterCombined(channel=channel, x=x)


@dataclass_param(params=ParameterCombined.product(list_x=params_x, channels=[0, 1]))
def test_y(param: ParameterCombined):
    """
    Negative: More code to type.
    Positive: Code is readable without knowing pytest internals.
    Positive: Full control over the 'id'.
    Positive: Full control over the markers.
    Positive: All code supports typehints.
    """
    assert param.x.a * param.x.b == param.x.expected_result
