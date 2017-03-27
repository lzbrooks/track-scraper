import logging
import requests
from bs4 import BeautifulSoup
import os


# Settings
os.environ['NO_PROXY'] = 'localhost'


def set_up_logging_file():
    logging.basicConfig(filename='web_scraper.log',
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    return logging


def set_up_logging_to_console():
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    return logging


def get_webpage_soup(webpage_url, proxy_settings):
    if proxy_settings[0] and proxy_settings[1]:
        webpage = requests.get(webpage_url, proxies=proxy_settings)
    else:
        webpage = requests.get(webpage_url)
    webpage_soup = BeautifulSoup(webpage.text, "html.parser")
    return webpage_soup
