__author__ = "Aron Kaufmann"

import copy, re
from urllib import request
from bs4 import BeautifulSoup, element


def fill_dummy(counter):
    print(counter)
    if counter == 0:
        return "position"
    elif counter % 2 == 0:
        return "institution"
    elif counter % 2 == 1:
        return "name"


def extract_organizers_info(url):
    organizers_dummy = {attribute: None for attribute in ["name", "position", "institution"]}
    organizers_info_list = []
    try:
        page = request.urlopen(url)
    except ConnectionError:
        print("Could not connect to url.")

    organizers = BeautifulSoup(page, 'html.parser').find("section", {"class": "content"})
    for child in organizers.findChildren('p'):
        print(child)
        print(child.text)
        text = re.sub(r"[</]", " </", str(child)).strip()
        text = re.sub(r"<.+?>", "", text).strip()
        print(re.split(r"\s{2,10}", text))
        #print(child.find('strong'))
        #print(child.findAll('em'))
        counter = 0
        # for tag in child.contents:
        #     if isinstance(tag, element.Tag):
        #         text = tag.text # re.sub(r"[\W^ ]", "", tag.text)
        #         if re.sub(r"[\W]", "", text) != "":
        #             print(text)
        #             organizers_dummy[fill_dummy(counter)] = text
        #             counter += 1
        #     elif isinstance(tag, element.NavigableString):
        #         text = re.sub(r"[^\w\s]", "", tag).strip()
        #         if text != "":
        #             print(text)
        #             organizers_dummy[fill_dummy(counter)] = text
        #             counter += 1
        # if counter > 1:
        #     organizers_info_list.append(copy.copy(organizers_dummy))
        # line = re.sub(r"<.+?>", "", tag)
        # print(line)
        # organizers_dummy['name'] = child.text.strip()
        # organizers_dummy['link'] = img_link

    return organizers_info_list


def get_organizers():
    organizers_info = extract_organizers_info("http://www.acl2019.org/EN/committees.xhtml")
    for t in organizers_info:
        print(t)
    return organizers_info


get_organizers()
