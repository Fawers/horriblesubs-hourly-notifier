import os
from xml.etree import ElementTree

import pytest

import guid


@pytest.fixture()
def partial_rss():
    return ElementTree.fromstring("""<rss version="2.0">
    <channel>
        <title>HorribleSubs RSS</title>
        <description>RSS feed for HorribleSubs releases in 720p.</description>
        <link>http://www.horriblesubs.info</link>
        <item>
            <title>[HorribleSubs] Ongaku Shoujo - 01 [720p].mkv</title>
            <link>magnet:?xt=urn:btih:BEETJVI3T3AXASP6KGZGVZK7IHLTA7ZO&amp;tr=http://nyaa.tracker.wf:7777/announce&amp;tr=udp://tracker.coppersurfer.tk:6969/announce&amp;tr=udp://tracker.internetwarriors.net:1337/announce&amp;tr=udp://tracker.leechersparadise.org:6969/announce&amp;tr=udp://tracker.opentrackr.org:1337/announce&amp;tr=udp://open.stealth.si:80/announce&amp;tr=udp://p4p.arenabg.com:1337/announce&amp;tr=udp://mgtracker.org:6969/announce&amp;tr=udp://tracker.tiny-vps.com:6969/announce&amp;tr=udp://peerfect.org:6969/announce&amp;tr=http://share.camoe.cn:8080/announce&amp;tr=http://t.nyaatracker.com:80/announce&amp;tr=https://open.kickasstracker.com:443/announce</link>
            <guid
                isPermaLink="false">BEETJVI3T3AXASP6KGZGVZK7IHLTA7ZO</guid>
                <pubDate>Sat, 07 Jul 2018 18:54:04 +0000</pubDate>
        </item>
        <item>
            <title>[HorribleSubs] Hyakuren no Haou to Seiyaku no Valkyria - 01 [720p].mkv</title>
            <link>magnet:?xt=urn:btih:ADISBI5CRITGTIC5CSKE4TMA7BQS6SYD&amp;tr=http://nyaa.tracker.wf:7777/announce&amp;tr=udp://tracker.coppersurfer.tk:6969/announce&amp;tr=udp://tracker.internetwarriors.net:1337/announce&amp;tr=udp://tracker.leechersparadise.org:6969/announce&amp;tr=udp://tracker.opentrackr.org:1337/announce&amp;tr=udp://open.stealth.si:80/announce&amp;tr=udp://p4p.arenabg.com:1337/announce&amp;tr=udp://mgtracker.org:6969/announce&amp;tr=udp://tracker.tiny-vps.com:6969/announce&amp;tr=udp://peerfect.org:6969/announce&amp;tr=http://share.camoe.cn:8080/announce&amp;tr=http://t.nyaatracker.com:80/announce&amp;tr=https://open.kickasstracker.com:443/announce</link>
            <guid
                isPermaLink="false">ADISBI5CRITGTIC5CSKE4TMA7BQS6SYD</guid>
                <pubDate>Sat, 07 Jul 2018 18:52:32 +0000</pubDate>
        </item>
        <item>
            <title>[HorribleSubs] Persona 5 The Animation - 14 [720p].mkv</title>
            <link>magnet:?xt=urn:btih:FYDRA5XVUJEG4DSMUDIBF4PJFHDMVHOC&amp;tr=http://nyaa.tracker.wf:7777/announce&amp;tr=udp://tracker.coppersurfer.tk:6969/announce&amp;tr=udp://tracker.internetwarriors.net:1337/announce&amp;tr=udp://tracker.leechersparadise.org:6969/announce&amp;tr=udp://tracker.opentrackr.org:1337/announce&amp;tr=udp://open.stealth.si:80/announce&amp;tr=udp://p4p.arenabg.com:1337/announce&amp;tr=udp://mgtracker.org:6969/announce&amp;tr=udp://tracker.tiny-vps.com:6969/announce&amp;tr=udp://peerfect.org:6969/announce&amp;tr=http://share.camoe.cn:8080/announce&amp;tr=http://t.nyaatracker.com:80/announce&amp;tr=https://open.kickasstracker.com:443/announce</link>
            <guid
                isPermaLink="false">FYDRA5XVUJEG4DSMUDIBF4PJFHDMVHOC</guid>
                <pubDate>Sat, 07 Jul 2018 17:01:53 +0000</pubDate>
        </item>
    </channel>
</rss>""")


@pytest.fixture()
def clean_guid_file():
    yield None
    os.remove(guid.FILEPATH)
