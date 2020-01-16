__author__ = "Aron Kaufmann"

import copy
from urllib import request
from bs4 import BeautifulSoup


def extract_tutorials_info(url):
    tutorial_dummy = {attribute: None for attribute in ["title", "authors", "abstract", "datetime", "location", "link"]}
    tutorial_info_list = []
    try:
        page = request.urlopen(url)
    except ConnectionError:
        print("Could not connect to url.")

    tutorials = BeautifulSoup(page, 'html.parser').find("section", {"id": "main_content"})
    for child in tutorials.findChildren('p'):
        text = child.text.split('\n')
        tutorial_dummy['title'] = text[0]
        tutorial_dummy['authors'] = text[1]
        tutorial_info_list.append(copy.copy(tutorial_dummy))
    return tutorial_info_list


def get_tutorials():
    tutorials_info = extract_tutorials_info("https://coling2020.org/pages/tutorials")
    # for t in tutorials_info:
    #     print(t)
    return tutorials_info


get_tutorials()
