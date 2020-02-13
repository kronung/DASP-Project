__author__ = "Aron Kaufmann"

import copy
from urllib import request
from bs4 import BeautifulSoup
import confcrawler.util.util as util
import re


def extract_paper_info(url):
    paper_dummy = {attribute: None for attribute in ["paper_title", "paper_authors", "paper_type", "paper_link",
                                                     "paper_time", "paper_keywords"]}
    paper_info_list = []
    try:
        page = request.urlopen(url)
    except ConnectionError:
        print("Could not connect to url.")

    papers = BeautifulSoup(page, 'html.parser').findAll("p", class_="paper-item")
    for paper in papers:
        paper_dummy["paper_title"] = util.basic_string_clean(paper.contents[0])
        authors_str = paper.contents[2].text
        authors_list = [author.strip() for author in re.split(r",|\sand\s", authors_str)]
        paper_dummy["paper_authors"] = authors_list
        paper_info_list.append(copy.copy(paper_dummy))
    return paper_info_list


def get_papers():
    papers_info = extract_paper_info("http://www.acl2019.org/EN/program/papers.xhtml")
    # for t in papers_info:
    #     print(t)
    return papers_info
