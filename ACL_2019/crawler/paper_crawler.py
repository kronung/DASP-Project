__author__ = "Aron Kaufmann"
import copy
from urllib import request
from bs4 import BeautifulSoup


def extract_paper_info(url):
    tutorial_dummy = {attribute: None for attribute in ["title", "authors"]}
    tutorial_info_list = []
    try:
        page = request.urlopen(url)
    except:
        print("Could not connect to url.")
    papers = BeautifulSoup(page, 'html.parser').findAll("p", class_="paper-item")
    for paper in papers:
        tutorial_dummy["title"] = paper.contents[0]
        tutorial_dummy["authors"] = paper.contents[2].text
        tutorial_info_list.append(copy.copy(tutorial_dummy))
    return tutorial_info_list


tutorials_info = extract_paper_info("http://www.acl2019.org/EN/program/papers.xhtml")
for t in tutorials_info:
    print(t)
