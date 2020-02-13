__author__ = "Aron Kaufmann"

import copy
from urllib import request
from bs4 import BeautifulSoup


def extract_organizers_info(url):
    organizers_dummy = {attribute: None for attribute in ['members', "link"]}
    organizers_info_list = []
    try:
        page = request.urlopen(url)
    except ConnectionError:
        print("Could not connect to url.")

    organizers = BeautifulSoup(page, 'html.parser').find("section", {"id": "organizers"})
    for child in organizers.findChildren('a'):
        # print(child)
        link = child.find("img")
        if link:
            img_link = "https://coling2020.org" + link["src"].strip()
            # print(child.text.strip() + " " + img_link)
            organizers_dummy['members'] = child.text.strip()
            organizers_dummy['link'] = img_link
            organizers_info_list.append(copy.copy(organizers_dummy))
    return organizers_info_list


def get_organizers():
    organizers_info = extract_organizers_info("https://coling2020.org/pages/organization")
    # for t in organizers_info:
    #     print(t)
    return organizers_info


get_organizers()
