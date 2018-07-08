import os
from xml.etree import ElementTree
from unittest.mock import MagicMock, patch

import requests

import hs.rss


@patch('requests.get')
def test_parse(request):
    with open(os.path.join('tests', 'templates', 'rss.xml')) as f:
        expected_rss = f.read()

    response = MagicMock(requests.Response)
    request.return_value = response
    response.text = expected_rss
    rss = hs.rss.parse()
    response.raise_for_status.assert_called_once()

    assert ElementTree.tostring(rss).decode() == expected_rss
