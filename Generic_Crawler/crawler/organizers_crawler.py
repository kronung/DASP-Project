"""Crawler to collect the EMNLP 2019 organizers """
__author__ = "Yuqing_Xu"

from urllib import request
import bs4
from bs4 import BeautifulSoup
import json

def extract_organizers(organizers_url):
    """
       Extracts all information available for organizers at
       https://www.emnlp-ijcnlp2019.org/calls/papers .
       :return: a list of a dictionary with organizers represented as one dictionary.
       """
    try:
        page = request.urlopen(organizers_url)
    except:
        print("Could not connect to url.")
        return []

    soup = BeautifulSoup(page, 'html.parser')

    for child in soup.findChildren('h2', id='organizers'):
        orgnizers1 = child.findNext("p").text.split("\n")[1:]
        orgnizers2 = child.findNext("p").findNext("p").text.split('\n')[1:]
        orgnizers3 = child.findNext("p").findNext("p").findNext("p").text.split('\n')[1:]
    organizers = orgnizers1 + orgnizers2 + orgnizers3
    #print(json.dumps(organizers_list, indent=1))
    return organizers


