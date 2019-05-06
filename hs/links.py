import re
import unicodedata
from typing import List
from datetime import timedelta

import redis


REPLACEMENT_PATTERN = re.compile(r'[^a-z0-9]')
ONE_DAY = timedelta(days=1)


def cache_from_releases(releases: List[dict]) -> None:
    """
    Caches links of entries from the daily releases.

    cache_from_releases is responsible for sanitizing each show name to pass as a Redis key name. The URL of the
    show is the value of the key. To keep it simple, key names will be in the form `hs:{SHOW}` where `SHOW`
    consists of only lower-case characters.

    releases is a list of dicts whose keys are `title`, `url`, and `time` (as defined in `main.daily_releases`).
    """
    client = redis.Redis()

    for release in (r for r in releases if r.get('url')):  # filter out releases without a url
        title = unicodedata.normalize('NFKD', release['title'].lower())
        title = REPLACEMENT_PATTERN.sub('', title)

        client.setex(f'hs:{title}', ONE_DAY, release['url'])


def get(key_name: str) -> str:
    "Gets and returns the value under `key_name` on Redis. Returns empty string if not found."
    return redis.Redis().get(key_name) or ''
