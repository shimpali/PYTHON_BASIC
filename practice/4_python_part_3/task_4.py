"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""

import argparse
import faker
from unittest import mock


def print_name_address(args: argparse.Namespace) -> None:
    fake = faker.Faker()
    for _ in range(args.number):
        print({args.name or 'some_name': fake.name(), args.address or 'some_address': fake.address()})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('number', type=int, help='positive number of generated instances')
    parser.add_argument('--address', help='key used in generated dict')
    parser.add_argument('--name', help='name of Faker provider')
    parser_args = parser.parse_args()
    print_name_address(parser_args)


"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""


@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(number=2, address='some_address', name='some_name'))
def test_print_name_address(mock_args):
    print_name_address(mock_args)