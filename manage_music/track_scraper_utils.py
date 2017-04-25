import requests
from bs4 import BeautifulSoup
import os


# Settings
os.environ['NO_PROXY'] = 'localhost'


def get_webpage_soup(webpage_url, proxy_settings):
    if proxy_settings[0] and proxy_settings[1]:
        webpage = requests.get(webpage_url, proxies=proxy_settings)
    else:
        webpage = requests.get(webpage_url)
    webpage_soup = BeautifulSoup(webpage.text, "html.parser")
    return webpage_soup
