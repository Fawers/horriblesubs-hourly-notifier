import bs4
import requests


URL = 'https://horriblesubs.info/'


def parse():
    response = requests.get(URL)
    response.raise_for_status()
    return bs4.BeautifulSoup(response.text, 'html.parser')
