__author__ = "Aron Kaufmann"

import copy, re
from urllib import request
from bs4 import BeautifulSoup, element

from confcrawler.util import util


def fill_dummy(counter):
    #print(counter)
    if counter == 0:
        return "position"
    elif counter % 2 == 0:
        return "institution"
    elif counter % 2 == 1:
        return "members"


def extract_organizers_info(url):
    organizers_dummy = {attribute: None for attribute in ["members", "position", "institution"]}
    organizers_info_list = []
    try:
        page = request.urlopen(url)
    except ConnectionError:
        print("Could not connect to url.")

    organizers = BeautifulSoup(page, 'html.parser').find("section", {"class": "content"})
    for child in organizers.findChildren('p'):
        counter = 0
        for tag in child.contents:
            if isinstance(tag, element.Tag):
                text = tag.text # re.sub(r"[\W^ ]", "", tag.text)
                if re.sub(r"[\W]", "", text) != "":
                    authors_str = util.basic_string_clean(text)
                    authors_list = [author.strip() for author in re.split(r",|\sand\s", authors_str)]
                    attribute = fill_dummy(counter)
                    if attribute == "members":
                        organizers_dummy[attribute] = authors_list
                    else:
                        organizers_dummy[attribute] = util.basic_string_clean(text)
                    counter += 1
            elif isinstance(tag, element.NavigableString):
                text = re.sub(r"[^\w\s]", "", tag).strip()
                if text != "":
                    authors_str = util.basic_string_clean(text)
                    authors_list = [author.strip() for author in re.split(r",|\sand\s", authors_str)]
                    attribute = fill_dummy(counter)
                    if attribute == "members":
                        organizers_dummy[attribute] = authors_list
                    else:
                        organizers_dummy[attribute] = util.basic_string_clean(text)
                    counter += 1
            if counter > 1 and organizers_dummy["members"] is not None and organizers_dummy["institution"] is not None:
                organizers_info_list.append(copy.copy(organizers_dummy))
                organizers_dummy["members"] = None
                organizers_dummy["institution"] = None
        organizers_dummy['members'] = util.basic_string_clean(child.text.strip())

    return organizers_info_list


def get_organizers():
    organizers_info = extract_organizers_info("http://www.acl2019.org/EN/committees.xhtml")
    return organizers_info


get_organizers()
