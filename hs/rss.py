from xml.etree import ElementTree

import requests


URL = 'http://www.horriblesubs.info/rss.php?res=720'


def parse():
    response = requests.get(URL)
    response.raise_for_status()
    return ElementTree.fromstring(response.text)
