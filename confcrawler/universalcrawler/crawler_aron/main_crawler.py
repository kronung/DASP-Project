"""Dynamic Crawler for collecting the (EM)NLP 2019 papers"""
__author__ = "Aron Kaufmann"


from bs4 import BeautifulSoup, element
from urllib import request
import re

papers_url = [("https://naacl2019.org/program/accepted/", ("section", "page__content"), "p"),
              ("https://www.emnlp-ijcnlp2019.org/program/tutorials/", ("section", "page__content"), "h3"),
              ("https://www.emnlp-ijcnlp2019.org/program/accepted/", ("section", "page__content"), "li")]
# emnlp     infopoint   <li>
#           anchor      <section class="page__content" itemprop="text">
# naacl     infopoint   <p>
#           anchor      section class="page__content" itemprop="text">


def crawl_info(url, anchor, info_point, extra_info=None, children=False):
    try:
        page = request.urlopen(url)
    except ConnectionError:
        print("Could not connect to url.")

    soup = BeautifulSoup(page, 'html.parser').find(anchor[0], {"class": anchor[1]})
    content = soup.findAll(info_point)
    info_list = []
    if children:
        print("children is True")
    elif extra_info is None:
        print("extra is None")
    elif extra_info and not children:
        print("extra is given w/o children")

    for info in content:
        if extra_info is None:
            info_list.append(info)
        elif children:
            children_info = []
            if extra_info:
                children = info.findChildren(extra_info, recursive=False)
            else:
                children = info.findChildren(recursive=False)
            for child in children:
                children_info.append(child)
            info_list.append(info + children_info)
        elif not children and extra_info is not None:
            extra_text = ""
            extras = info.findNext(extra_info)
            while extras and extras.name == extra_info:
                # print(extras.name, extras, extras.contents)
                extra_text += extras.text + "|||"
                extras = extras.find_next_sibling()
            info_list.append((info, extra_text))
    return info_list


# infos = crawl_info(papers_url[0][0], papers_url[0][1], papers_url[0][2])
infos = crawl_info(papers_url[1][0], papers_url[1][1], papers_url[1][2], "p")
# infos = crawl_info(papers_url[2][0], papers_url[2][1], papers_url[2][2])
for i in infos:
    if isinstance(i, element.Tag):
        print(i.text, '\n-----------------------')
    else:
        print(type(i))
        print(i, '\n-----------------------')
