import os
from xml.etree import ElementTree

import pytest

import guid


@pytest.fixture(scope='session')
def rss_xml(rss_xml_raw):
    return ElementTree.fromstring(rss_xml_raw)


@pytest.fixture(scope='session')
def rss_xml_raw():
    with open(os.path.join('tests', 'templates', 'rss.xml.template')) as f:
        return f.read()


@pytest.fixture(scope='session')
def frontpage_html_raw():
    with open(os.path.join('tests', 'templates', 'frontpage.html.template')) as f:
        return f.read()


@pytest.fixture
def clean_guid_file():
    yield None
    os.remove(guid.FILEPATH)
