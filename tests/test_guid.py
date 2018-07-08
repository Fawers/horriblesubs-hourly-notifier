from unittest import mock

import pytest

import guid


def test_read():
    with mock.patch('builtins.open', mock.mock_open(read_data='BEETJVI3T3AXASP6KGZGVZK7IHLTA7ZO')):
        assert guid.read() == 'BEETJVI3T3AXASP6KGZGVZK7IHLTA7ZO'


@pytest.mark.usefixtures('clean_guid_file')
@pytest.mark.parametrize('string,length', [
    ('test string', len('test string')),
    ('dummy', len('dummy')),
    ('lalilulelo', len('lalilulelo')),
    ("let us test now", len("let us test now")),
])
def test_write(string, length):
    assert guid.write(string) == length
