import re
from itertools import takewhile
from xml.etree.ElementTree import Element

import hs.rss
import guid as guidfile
from telegram import bot


PATTERN = re.compile(r'^\[HorribleSubs\] (?P<title>.*?) \[720p\]\.mkv$')


def determine_last_show(rss: Element, guid: str) -> Element:
    return rss.find('channel/item/[guid="{}"]'.format(guid))


def hourly_releases():
    rss = hs.rss.parse()
    newest_guid = rss.find('channel/item/guid').text
    last_guid = guidfile.read()

    if newest_guid == last_guid:  # no new entries since last run
        return []

    halt_point = determine_last_show(rss, last_guid)

    entries = takewhile(lambda e: e is not halt_point, rss.iterfind('channel/item'))
    releases = [PATTERN.match(entry.find('title').text).group('title') for entry in entries]
    guidfile.write(newest_guid)
    return releases


def daily_releases():
    pass


if __name__ == '__main__':
    releases = hourly_releases()

    if releases:
        bot.send_to_channel('\n'.join(releases))
