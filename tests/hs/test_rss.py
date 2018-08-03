from unittest.mock import MagicMock, patch

import requests

import hs.rss


@patch('requests.get')
def test_parse(get: MagicMock, rss_xml_raw):
    response = MagicMock(requests.Response)
    get.return_value = response
    response.text = rss_xml_raw
    rss = hs.rss.parse()

    get.assert_called_once_with(hs.rss.URL)
    response.raise_for_status.assert_called_once()
    assert len(rss.findall('.//item')) == 51
