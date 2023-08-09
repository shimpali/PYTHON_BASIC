"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     >>> math_calculate('log', 1024, 2)
     10.0
     >>> math_calculate('ceil', 10.7)
     11
"""
import math
import pytest


class OperationNotFoundException(Exception):
    pass


def math_calculate(function: str, *args):
    try:
        if 1 <= len(args) <= 2:
            return getattr(math, function)(*args)
    except AttributeError:
        raise OperationNotFoundException('Operation not found!')


"""
Write tests for math_calculate function
"""


def test_math_calculate():
    assert math_calculate('log', 1024, 2) == 10.0
    assert math_calculate('ceil', 10.7) == 11
    with pytest.raises(OperationNotFoundException):
        math_calculate('something', 10)
