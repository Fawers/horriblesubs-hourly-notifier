import main
from unittest.mock import patch

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
def test_hourly_releases_returns_empty_list(mock, partial_rss):
    with patch('hs.rss.parse', return_value=partial_rss):
        assert len(main.hourly_releases()) == 0


@pytest.mark.usefixtures('clean_guid_file')
@patch('guid.read', return_value='')
def test_hourly_releases_returns_all_entries(mock, partial_rss):
    with patch('hs.rss.parse', return_value=partial_rss):
        releases = main.hourly_releases()
        assert len(releases) == 3
        assert releases == ['Ongaku Shoujo - 01', 'Hyakuren no Haou to Seiyaku no Valkyria - 01', 'Persona 5 The Animation - 14']


@pytest.mark.usefixtures('clean_guid_file')
@patch('guid.read', return_value='FYDRA5XVUJEG4DSMUDIBF4PJFHDMVHOC')
def test_hourly_releases_returns_two_newest_entries(mock, partial_rss):
    with patch('hs.rss.parse', return_value=partial_rss):
        releases = main.hourly_releases()
        assert len(releases) == 2
        assert releases == ['Ongaku Shoujo - 01', 'Hyakuren no Haou to Seiyaku no Valkyria - 01']
