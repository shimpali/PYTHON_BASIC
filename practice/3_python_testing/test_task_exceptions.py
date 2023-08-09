"""
Write tests for division() function in 2_python_part_2/task_exceptions.py
In case (1,1) it should check if exception were raised
In case (1,0) it should check if return value is None and "Division by 0" printed
If other cases it should check if division is correct

TIP: to test output of print() function use capfd fixture
https://stackoverflow.com/a/20507769
"""
import pytest
from tasks.task_exceptions import division, DivisionByOneException


def test_division_ok(capfd):
    assert division(2, 2) == 1
    out, err = capfd.readouterr()
    assert out == 'Division finished\n'


def test_division_by_zero(capfd):
    assert division(5, 0) is None
    out, err = capfd.readouterr()
    assert out == 'Division by 0\nDivision finished\n'


def test_division_by_one(capfd):
    with pytest.raises(DivisionByOneException) as error:
        division(5, 1)
    out, err = capfd.readouterr()
    assert out.strip() == 'Division finished'
    assert 'Deletion on 1 get the same result' in str(error.value)
