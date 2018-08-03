import os
import re
from itertools import takewhile
from xml.etree.ElementTree import Element

import hs
import guid as guidfile
from telegram import bot


PATTERN = re.compile(r'^\[HorribleSubs\] (?P<title>.*?) \[720p\](?:\.mkv| \(Batch\))$')


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
    # this function MUST run ONLY at 00:00 PST/PDT, or whatever timezone HorribleSubs is in.
    soup = hs.frontpage.parse()
    schedule = soup.select_one('table.schedule-table')
    releases = []

    for release_data in schedule.select('td'):
        if 'schedule-widget-show' in release_data['class']:
            a = release_data.select_one('a')
            data = {'title': a.text, 'url': a.get('href', '')}

        elif 'schedule-widget-time' in release_data['class']:
            data['time'] = release_data.text
            releases.append(data)

    return releases


def format_dailies(releases):
    return [f"[{r['title']}](https://horriblesubs.info{r['url']}) in {r['time'].replace(':', 'h')}m" for r in releases]


if __name__ == '__main__':
    if 'daily' in os.sys.argv:
        releases = ['Releases in the next 24 hours:'] + format_dailies(daily_releases())

    else:
        releases = hourly_releases()

    if releases:
        bot.send_to_channel('\n'.join(releases))
