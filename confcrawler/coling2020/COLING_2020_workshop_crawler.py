"""Crawler to collect the COLING 2020 workshops"""
__author__ = "Yuqing Xu"

from bs4 import BeautifulSoup
from urllib import request
import json


def extract_workshops(url):
    """
    Extracts all information available for workshops provided at
    https://coling2020.org/pages/workshops
    :return: list of dictionaries with a workshop represented as one dictionary.
    """
    workshops = []
    # url = "https://coling2020.org/pages/workshops"

    try:
        page = request.urlopen(url)
    except:
        print("Could not connect to url.")

    soup = BeautifulSoup(page, 'html.parser').find("section", {"id": "main_content"})

    for child in soup.findChildren('h3'):
        for i in child.findNext('ul').find_all('li'):
            workshop = {attribute: None for attribute in
                        ['title', 'authors', 'abstract', 'datetime', 'location', 'link']}
            workshop['datetime'] = child.text
            workshop['title'] = i.find('a').text
            workshop['link'] = i.find('a')['href']
            workshops.append(workshop)

    #print(json.dumps(workshops, indent=1))
    return workshops


def get_workshops():
    workshops_info = extract_workshops("https://coling2020.org/pages/workshops")
    # for t in workshops_info:
    #     print(t)
    return workshops_info


get_workshops()