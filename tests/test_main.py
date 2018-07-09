import main
from unittest.mock import patch

import bs4

import pytest


@pytest.mark.parametrize('input,expected', [
    ('[HorribleSubs] Ongaku Shoujo - 01 [720p].mkv', 'Ongaku Shoujo - 01'),
    ('[HorribleSubs] Hyakuren no Haou to Seiyaku no Valkyria - 01 [720p].mkv', 'Hyakuren no Haou to Seiyaku no Valkyria - 01'),
    ('[HorribleSubs] Persona 5 The Animation - 14 [720p].mkv', 'Persona 5 The Animation - 14'),
    ('[HorribleSubs] Hataraku Saibou - 01 [720p].mkv', 'Hataraku Saibou - 01'),
    ('[HorribleSubs] Darling in the FranXX - 24 [720p].mkv', 'Darling in the FranXX - 24')
])
def test_pattern(input, expected):
    assert main.PATTERN.match(input).group('title') == expected


@patch('guid.read', return_value='BEETJVI3T3AXASP6KGZGVZK7IHLTA7ZO')
def test_hourly_releases_returns_empty_list(mock, rss_xml):
    with patch('hs.rss.parse', return_value=rss_xml):
        assert len(main.hourly_releases()) == 0


@pytest.mark.usefixtures('clean_guid_file')
@patch('guid.read', return_value='')
def test_hourly_releases_returns_all_entries(mock, rss_xml):
    with patch('hs.rss.parse', return_value=rss_xml):
        releases = main.hourly_releases()
        assert len(releases) == 50
        assert releases[:3] == ['Ongaku Shoujo - 01', 'Hyakuren no Haou to Seiyaku no Valkyria - 01', 'Persona 5 The Animation - 14']


@pytest.mark.usefixtures('clean_guid_file')
@patch('guid.read', return_value='FYDRA5XVUJEG4DSMUDIBF4PJFHDMVHOC')
def test_hourly_releases_returns_two_newest_entries(mock, rss_xml):
    with patch('hs.rss.parse', return_value=rss_xml):
        releases = main.hourly_releases()
        assert len(releases) == 2
        assert releases == ['Ongaku Shoujo - 01', 'Hyakuren no Haou to Seiyaku no Valkyria - 01']


def test_daily_releases_return_all_entries(frontpage_html_raw):
    with patch('hs.frontpage.parse', return_value=bs4.BeautifulSoup(frontpage_html_raw, 'html.parser')):
        releases = main.daily_releases()

    assert releases == [
        {'title': 'Asobi Asobase', 'url': '/shows/asobi-asobase', 'time': '06:00'},
        {'title': 'Island', 'url': '/shows/island', 'time': '07:30'},
        {'title': 'Planet With', 'url': '/shows/planet-with', 'time': '07:30'},
        {'title': 'Hanebado!', 'url': '/shows/hanebado', 'time': '09:00'},
        {'title': "Chi's Sweet Adventure S2", 'url': '/shows/chis-sweet-adventure-s2', 'time': '11:00'},
        {'title': 'Gintama', 'url': '/shows/gintama', 'time': '11:00'}
    ]


@pytest.mark.parametrize('input,expected', [
    ([{'title': 'Island', 'url': '/shows/island', 'time': '07:30'}], ['[Island](https://horriblesubs.info/shows/island) in 07h30m']),
    ([{'title': 'Gintama', 'url': '/shows/gintama', 'time': '11:00'}], ['[Gintama](https://horriblesubs.info/shows/gintama) in 11h00m'])
])
def test_format_dailies(input, expected):
    assert main.format_dailies(input) == expected
