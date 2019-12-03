"""Crawler to collect the EMNLP 2019 tutorials"""
__author__ = "Lars Meister"

from bs4 import BeautifulSoup
from urllib import request
import json


def extract_tutorials():
    """
    Extracts all information available for tutorials provided at
    https://www.emnlp-ijcnlp2019.org/program/tutorials/ and
    https://www.emnlp-ijcnlp2019.org/program/ischedule/
    :return: list of dictionaries with a tutorial represented as one dictionary.
    """
    tutorials = []
    tutorial_reference = {}
    url = "https://www.emnlp-ijcnlp2019.org/program/tutorials/"

    try:
        page = request.urlopen(url)
    except:
        print("Could not connect to url.")

    soup = BeautifulSoup(page, 'html.parser').find("section", {"class": "page__content"})

    reference_counter = 0

    for child in soup.findChildren("h3")[2:]:
        tutorial = {attribute: None for attribute in ["title", "authors", "abstract", "datetime",
                                                           "location", "link"]}
        if child.text.split(" ")[0] in tutorial_reference:
            continue
        tutorial["title"] = child.text
        tutorial["authors"] = child.findNext("p").text.replace(" and ", ", ").split(", ")
        next_node = child.findNext("p").findNext("p")
        abstract = ""
        while next_node.name == "p":
            abstract += next_node.text + " "
            next_node = next_node.findNext()

        tutorial["abstract"] = abstract[:-1]
        tutorials.append(tutorial)
        tutorial_reference[child.text.split(" ")[0]] = reference_counter
        reference_counter += 1

    url = "https://www.emnlp-ijcnlp2019.org/program/ischedule/"

    try:
        page = request.urlopen(url)
    except:
        print("Could not connect to url.")

    tutorial_sessions = BeautifulSoup(page, 'html.parser')\
        .findAll("div", {"class": "session session-expandable session-tutorials"})

    for session in tutorial_sessions:
        time = session.find("span", {"class" : "session-time"})
        datetime = time["title"] + ", " + time.text
        for child in session.findChildren("span", {"class": "tutorial-title"}):
            title = child.find("strong").text.split(" ")[0]
            location = child.findNext("span", {"class" : "btn"}).text
            goal_index = tutorial_reference[title]
            if tutorials[goal_index]["datetime"] is None:
                tutorials[goal_index]["datetime"] = datetime
                tutorials[goal_index]["location"] = location
            else:
                cur_datetime = tutorials[goal_index]["datetime"] + ", " + time.text
                tutorials[goal_index]["datetime"] = cur_datetime

    return tutorials

