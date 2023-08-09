"""
Write a function that makes a request to some url
using urllib. Return status code and decoded response data in utf-8
Examples:
     >>> make_request('https://www.google.com')
     200, 'response data'
"""
from typing import Tuple
from urllib import request
from unittest.mock import patch, MagicMock


def make_request(url: str) -> Tuple[int, str]:
    try:
        req = request.Request(url)
        with request.urlopen(req) as response:
            return response.status, response.read().decode('utf-8')
    except Exception as e:
        print(e)


"""
Write test for make_request function
Use Mock for mocking request with urlopen https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'

   Ref- https://stackoverflow.com/a/34929900
"""


@patch('urllib.request.urlopen')
def test_make_request(mock_urlopen):
    cm = MagicMock()
    cm.getcode.return_value = 200
    cm.read.return_value = 'response data'
    cm.__enter__.return_value = cm
    mock_urlopen.return_value = cm

    with request.urlopen('http://test_url') as response:
        assert response.getcode() == 200
        assert response.read() == 'response data'