import os
import re
from itertools import takewhile
from datetime import datetime, timezone
from xml.etree.ElementTree import Element

import hs
import guid as guidfile
from telegram import bot


PATTERN = re.compile(r'^\[HorribleSubs\] (?P<title>.*?) \[720p\](?:\.mkv| \(Batch\))$')
HORRIBLE_SUBS = 'https://horriblesubs.info'


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
    releases = (PATTERN.match(entry.find('title').text).group('title').rpartition(' - ') for entry in entries)
    guidfile.write(newest_guid)
    return releases


def daily_releases():
    # this function MUST run ONLY at 00:00 PST/PDT, or whatever timezone HorribleSubs is in.
    soup = hs.frontpage.parse()
    schedule = soup.select_one('table.schedule-table')
    releases = []

    for release_data in schedule.select('td'):
        if 'schedule-widget-show' in release_data['class']:
            # On the event that there is no <a> present in a node, fall back to setting `a` to `release_data` itself
            a = release_data.select_one('a') or release_data
            data = {'title': a.text, 'url': a.get('href', '')}
            # I would love to treat this generically, but didn't find a way to bypass Cloufare.
            # Which is good in a way, it means that the tool they develop and maintain works.
            if 'idolmster' in data['url']:
                data['title'] = data['title'].replace('[email\xa0protected]', 'iDOLM@STER')

        elif 'schedule-widget-time' in release_data['class']:
            data['time'] = release_data.text
            releases.append(data)

    return releases


def format_dailies(releases, now):
    output = []
    time_format = '%H:%M %Z'

    for release in releases:
        time_local = release['time'].split(':')
        time_local = now.replace(hour=int(time_local[0]), minute=int(time_local[1]))
        time_utc = time_local.astimezone(timezone.utc)

        output.append("[{title}]({url}) at {local} ({utc})".format(
            title=release['title'],
            url=HORRIBLE_SUBS + release['url'],
            local=time_local.strftime(time_format),
            utc=time_utc.strftime(time_format)))

    return output


if __name__ == '__main__':
    if 'daily' in os.sys.argv:
        now = datetime.now().astimezone()
        releases = daily_releases()
        hs.links.cache_from_releases(releases)

        releases = [
            now.strftime('#%A, %-m/%-d').lower(),
            'Releases in the next 24 hours (estimates):',
        ] + format_dailies(releases, now)

    else:
        releases = hs.links.get_from_releases(hourly_releases())

    if releases:
        bot.send_to_channel('\n'.join(releases))
