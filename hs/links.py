import os
import re
from typing import List, Tuple
from datetime import timedelta
from unicodedata import normalize

import redis


REPLACEMENT_PATTERN = re.compile(r'[^a-z0-9]')
ONE_DAY = timedelta(days=1)


def _title_to_key(title: str) -> str:
    return 'hs:' + REPLACEMENT_PATTERN.sub(
        '',
        normalize('NFKD', title).lower())


def cache_from_releases(releases: List[dict]) -> None:
    """
    Caches links of entries from the daily releases.

    cache_from_releases is responsible for sanitizing each show name to pass as a Redis key name. The URL of the
    show is the value of the key. To keep it simple, key names will be in the form `hs:{SHOW}` where `SHOW`
    consists of only lower-case characters.

    releases is a list of dicts whose keys are `title`, `url`, and `time` (as defined in `main.daily_releases`).
    """
    client = redis.Redis(host=os.environ.get('REDIS_HOST', 'localhost'))

    for release in (r for r in releases if r.get('url')):  # filter out releases without a url
        key_name = _title_to_key(release['title'])
        client.setex(key_name, ONE_DAY, release['url'])


def get_from_releases(releases: List[Tuple[str, str, str]]) -> List[str]:
    """
    Gets available links for the given releases and returns them markdown-formatted.

    get_from_releases takes a list of releases generated in `main.hourly_releases` and checks for the existence
    of keys whose names correspond to the names of each release. The output is a markdown-formatted string
    created from the URL to the release and its name when the key exists, or just the release itself otherwise.
    """
    output = []
    client = redis.Redis(host=os.environ.get('REDIS_HOST', 'localhost'))

    for release in releases:
        key_name = _title_to_key(release[0])
        url = client.get(key_name)

        if url is not None:
            output.append('<a href="https://horriblesubs.info{url}">{0}</a> – {2}'.format(*release, url=url.decode()))

        else:
            output.append(''.join(release))

    return output
