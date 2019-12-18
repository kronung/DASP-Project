"""Crawler to collect the EMNLP 2019 topics"""
__author__ = "Yuqing_Xu"

from urllib import request
from bs4 import BeautifulSoup
import logging
import json
logger = logging.getLogger("topics_crawler")

def extract_topics(topics_url):
    """
    Extracts all information available for topics at
    https://www.emnlp-ijcnlp2019.org/calls/papers .
    :return: a list of a dictionary with a topic represented as one dictionary.
    """
    logger.info('Start crawling TOPICS...')
    logger.info('Crawling data from: %s', topics_url)
    try:
        page = request.urlopen(topics_url)
    except:
        logger.warning("URl could not be crawled!")
        return []
    soup = BeautifulSoup(page, 'html.parser')

    strings = soup.select("section > ul")[0].get_text()
    topics = strings.split('\n')
    topics = [i for i in topics if i != '']
    #print(json.dumps(topic_list, indent=1))
    logger.info('Crawling TOPICS DONE')
    return topics

