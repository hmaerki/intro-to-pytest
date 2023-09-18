try:
    # Python 3.8 and newer
    from typing import Protocol
except:
    # Python 3.7
    from typing_extensions import Protocol

from typing import Iterator, List, Optional


import pytest
import _pytest


class ParamProtocol(Protocol):
    '''

    '''
    @property
    def id(self) -> str:
        '''
        The test identifier
        '''
        ...

    @property
    def id_note(self) -> Optional[str]:
        '''
        Add a note if something is very special about this test.
        '''
        ...

    @property
    def marks(self) -> Optional[List[pytest.Mark]]:
        '''
        Marks to be applied to the test
        '''
        ...


def dataclass_param(params: List[ParamProtocol]):
    '''
    This decorator may be used in the same way as '@pytest.mark.parametrize(...)'.
    However, the parameters must implement 'ParamProtocol'.
    '''
    def add_markers() -> Iterator[_pytest.mark.structures.ParameterSet]:
        for parameter in params:
            marks = ()
            marks_text = ""
            if parameter.marks is not None:
                marks = parameter.marks
                assert isinstance(marks, (list, tuple)), marks
                marks_text = ",".join([m.name for m in marks])
                marks_text = f" ({marks_text})"
            if parameter.id_note is not None:
                marks_text = f" {marks_text} {parameter.id_note}"
            yield pytest.param(
                parameter,
                marks=marks,
                id=parameter.id + marks_text,
            )

    args = ("param", add_markers())
    mark = pytest.Mark("parametrize", args, kwargs={}, _ispytest=True)
    return pytest.MarkDecorator(mark, _ispytest=True)
