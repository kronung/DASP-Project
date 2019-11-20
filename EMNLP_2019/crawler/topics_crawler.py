"""Crawler to collect the EMNLP 2019 topics"""
__author__ = "Yuqing_Xu"

import requests
import bs4
from bs4 import BeautifulSoup
import json

def topics_crawler():
    """
    Extracts all information available for topics at
    https://www.emnlp-ijcnlp2019.org/calls/papers .
    :return: a list of a dictionary with a topic represented as one dictionary.
    """
    page = requests.get("https://www.emnlp-ijcnlp2019.org/calls/papers")
    soup = BeautifulSoup(page.content, 'html.parser')

    topic_list = []
    strings = soup.select("section > ul")[0].get_text()
    array = strings.split('\n')
    array = [i for i in array if i != '']
    dic = {'topics':array}
    topic_list.append(dic)
    #print(topic_list)
    #print(json.dumps(topic_list, indent=1))
    return topic_list
