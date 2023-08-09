"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""
from unittest.mock import patch
from tasks.task_input_output import read_numbers


@patch('builtins.input')
def test_read_numbers_without_text_input(input_values):
    input_values.side_effect = [1, 2, 2]
    assert read_numbers(3) == 'Avg: 1.67'


@patch('builtins.input')
def test_read_numbers_with_text_input(input_values):
    input_values.side_effect = [1, 2, 'Hello']
    assert read_numbers(3) == 'Avg: 1.5'
