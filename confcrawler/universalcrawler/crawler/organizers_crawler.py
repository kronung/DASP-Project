"""Crawler to collect the EMNLP 2019 organizers """
__author__ = "Yuqing_Xu"

from urllib import request
import logging
from bs4 import BeautifulSoup
import json

logger = logging.getLogger("organizers_crawler")

def extract_organizers(organizers_url):
    """
    Extracts all information available for organizers at
    https://www.emnlp-ijcnlp2019.org/calls/papers .
    :return: a list of a dictionary with organizers represented as one dictionary.
    """
    logger.info('Start crawling ORGANIZERS...')
    logger.info('Crawling data from: %s', organizers_url)
    try:
        page = request.urlopen(organizers_url)
    except:
        logger.warning("URl could not be crawled!")
        return []

    soup = BeautifulSoup(page, 'html.parser')
    orgnizers1 = []
    orgnizers2 = []
    orgnizers3 = []

    for child in soup.findChildren('h2', id='organizers'):
        orgnizers1 = child.findNext("p").text.split("\n")[1:]
        orgnizers2 = child.findNext("p").findNext("p").text.split('\n')[1:]
        orgnizers3 = child.findNext("p").findNext("p").findNext("p").text.split('\n')[1:]
    organizers = orgnizers1 + orgnizers2 + orgnizers3
    logger.info('Crawling ORGANIZERS DONE')
    #print(json.dumps(organizers_list, indent=1))
    return organizers


