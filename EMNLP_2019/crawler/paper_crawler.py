"""Crawler to collect the EMNLP 2019 papers"""
__author__ = "Lars Meister"

from bs4 import BeautifulSoup
from urllib import request
import json


def extract_papers():
    """
    Extracts all information available for papers provided at
    https://www.emnlp-ijcnlp2019.org/program/accepted/ and
    https://www.emnlp-ijcnlp2019.org/program/ischedule/
    :return: list of dictionaries with a paper represented as one dictionary.
    """
    papers = []
    paper_reference = {}

    # crawl the papers site
    # extract title, authors and group for each paper
    url = "https://www.emnlp-ijcnlp2019.org/program/accepted/"

    try:
        page = request.urlopen(url)
    except:
        print("Could not connect to url.")

    soup = BeautifulSoup(page, 'html.parser').find("section", {"class": "page__content"})

    reference_counter = 0

    for child in soup.findAll("h2"):
        paper_type = child.text
        for paper_entry in child.findNext('ul').findChildren("li"):
            paper = {attribute: None for attribute in ["title", "authors", "type", "link",
                                                       "datetime", "topic"]}
            paper["type"] = paper_type
            paper["title"] = paper_entry.span.text.replace("\t", "")
            paper["authors"] = paper_entry.i.text.replace(' and ', ', ').replace("\t", "").split(
                ', ')
            papers.append(paper)
            paper_reference[paper_entry.span.text.replace("\t", "").replace("’", "'").lower()] = \
                reference_counter
            paper_reference[paper_entry.i.text.replace(' and ', ', ').replace("\t",
                                                                              "")] = \
                reference_counter
            reference_counter += 1

    # crawl the schedule site and merge results
    # try to extract link, datetime and category topics and merge with existing papers
    url = "https://www.emnlp-ijcnlp2019.org/program/ischedule/"

    try:
        page = request.urlopen(url)
    except:
        print("Could not connect to url.")

    paper_sessions = BeautifulSoup(page, 'html.parser') \
        .findAll("div", {"class": "session-box"})

    for session in paper_sessions:
        for box in session.findChildren("div", {"class": "session"}):
            box_type = "paper"
            topic = box.find("a", {"class": "session-title"}).text.split(": ")[1]
            time = box.find("span", {"class": "session-time"})
            datetime = time["title"] + ", " + time.text
            # session poster
            if box.get("class")[2] == "session-posters":
                box_type = "poster"
            for paper in box.findChildren("tr", {"id": box_type}):
                title = paper.find("span", {"class": box_type + "-title"}).text[:-2].lower()\
                    .replace("`", "\"")
                try:
                    goal_index = paper_reference[title]
                    papers[goal_index]["datetime"] = datetime
                    papers[goal_index]["topic"] = topic
                    papers[goal_index]["link"] = paper.find("i")['data']
                except KeyError:
                    try:
                        goal_index = paper_reference[paper.find("em").text.replace(' and ', ', ')]
                        papers[goal_index]["datetime"] = datetime
                        papers[goal_index]["topic"] = topic
                        papers[goal_index]["link"] = paper.find("i")['data']
                    except KeyError:
                        print("KeyException[ " + title + " ] not found in papers!")


    #print(json.dumps(papers, indent=1))
    return papers

