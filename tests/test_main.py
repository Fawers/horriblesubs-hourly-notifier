from unittest.mock import patch
from datetime import datetime, timedelta, timezone

import bs4
import pytest

import main


@pytest.mark.parametrize('input,expected', [
    ('[HorribleSubs] Ongaku Shoujo - 01 [720p].mkv', 'Ongaku Shoujo - 01'),
    ('[HorribleSubs] Hyakuren no Haou to Seiyaku no Valkyria - 01 [720p].mkv', 'Hyakuren no Haou to Seiyaku no Valkyria - 01'),
    ('[HorribleSubs] Persona 5 The Animation - 14 [720p].mkv', 'Persona 5 The Animation - 14'),
    ('[HorribleSubs] Hataraku Saibou - 01 [720p].mkv', 'Hataraku Saibou - 01'),
    ('[HorribleSubs] Darling in the FranXX - 24 [720p].mkv', 'Darling in the FranXX - 24'),
    ('[HorribleSubs] Sword Gai The Animation S2 (01-12) [720p] (Batch)', 'Sword Gai The Animation S2 (01-12)')
])
def test_pattern(input, expected):
    assert main.PATTERN.match(input).group('title') == expected


@patch('guid.read', return_value='YBHKMWWD7UDXBB24C7Z6CV325XUU3VKQ')
def test_hourly_releases_returns_empty_list(mock, rss_xml):
    with patch('hs.rss.parse', return_value=rss_xml):
        assert len(list(main.hourly_releases())) == 0


@pytest.mark.usefixtures('clean_guid_file')
@patch('guid.read', return_value='')
def test_hourly_releases_returns_all_entries(mock, rss_xml):
    with patch('hs.rss.parse', return_value=rss_xml):
        releases = list(main.hourly_releases())
        assert len(releases) == 51
        assert releases[:3] == [
            ('', '', 'Sword Gai The Animation S2 (01-12)'), ('Ongaku Shoujo', ' - ', '01'),
            ('Hyakuren no Haou to Seiyaku no Valkyria', ' - ', '01')
        ]


@pytest.mark.usefixtures('clean_guid_file')
@patch('guid.read', return_value='ADISBI5CRITGTIC5CSKE4TMA7BQS6SYD')
def test_hourly_releases_returns_two_newest_entries(mock, rss_xml):
    with patch('hs.rss.parse', return_value=rss_xml):
        releases = list(main.hourly_releases())
        assert len(releases) == 2
        assert releases == [('', '', 'Sword Gai The Animation S2 (01-12)'), ('Ongaku Shoujo', ' - ', '01')]


def test_daily_releases_return_all_entries(frontpage_html_raw):
    with patch('hs.frontpage.parse', return_value=bs4.BeautifulSoup(frontpage_html_raw, 'html.parser')):
        releases = main.daily_releases()

    assert releases == [
        {'title': 'Asobi Asobase', 'url': '/shows/asobi-asobase', 'time': '06:00'},
        {'title': 'Island', 'url': '/shows/island', 'time': '07:30'},
        {'title': 'Planet With', 'url': '/shows/planet-with', 'time': '07:30'},
        {'title': 'Hanebado!', 'url': '/shows/hanebado', 'time': '09:00'},
        {'title': "Chi's Sweet Adventure S2", 'url': '/shows/chis-sweet-adventure-s2', 'time': '11:00'},
        {'title': 'Gintama', 'url': '/shows/gintama', 'time': '11:00'},
        {'time': '05:55', 'title': 'THE iDOLM@STER CINDERELLA GIRLS Theater (TV)', 'url': '/shows/the-idolmster-cinderella-girls-theater'}
    ]


@pytest.mark.parametrize('input,expected', [
    ([{'title': 'Island', 'url': '/shows/island', 'time': '07:30'}], ['[Island](https://horriblesubs.info/shows/island) at 07:30 PDT (14:30 UTC)']),
    ([{'title': 'Gintama', 'url': '/shows/gintama', 'time': '11:00'}], ['[Gintama](https://horriblesubs.info/shows/gintama) at 11:00 PDT (18:00 UTC)']),
    ([{'time': '05:55', 'title': 'THE iDOLM@STER CINDERELLA GIRLS Theater (TV)', 'url': '/shows/the-idolmster-cinderella-girls-theater'}],
     ['[THE iDOLM@STER CINDERELLA GIRLS Theater (TV)](https://horriblesubs.info/shows/the-idolmster-cinderella-girls-theater) at 05:55 PDT (12:55 UTC)'])
])
def test_format_dailies(input, expected):
    now = datetime(2019, 5, 5, 0, 5, tzinfo=timezone(timedelta(hours=-7), 'PDT'))
    assert main.format_dailies(input, now) == expected
