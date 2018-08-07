from unittest.mock import patch, MagicMock

import requests

import hs


@patch('requests.get')
def test_parse(get: MagicMock, frontpage_html_raw):
    response = MagicMock(requests.Response)
    get.return_value = response
    response.text = frontpage_html_raw
    soup = hs.frontpage.parse()

    get.assert_called_once_with(hs.frontpage.URL)
    response.raise_for_status.assert_called_once()
    assert len(soup.select('.schedule-table td')) == 14
