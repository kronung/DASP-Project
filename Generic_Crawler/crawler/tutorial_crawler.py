"""Crawler to collect the EMNLP 2019 tutorials"""
__author__ = "Lars Meister"

from bs4 import BeautifulSoup
from urllib import request
import json
import re

def extract_tutorials(tutorials_url, schedule_url=None):
    """
    Extracts all information available for tutorials provided at
    https://www.emnlp-ijcnlp2019.org/program/tutorials/ and
    https://www.emnlp-ijcnlp2019.org/program/ischedule/
    :return: list of dictionaries with a tutorial represented as one dictionary.
    """
    tutorials = []
    tutorial_reference = {}
    #url = "https://www.emnlp-ijcnlp2019.org/program/tutorials/"

    # information from tutorial site

    try:
        page = request.urlopen(tutorials_url)
    except:
        print("Could not connect to url.")

    soup = BeautifulSoup(page, 'html.parser').find("section", {"class": "page__content"})

    reference_counter = 0
    for item in soup.find_all(['h2', 'h3'], id= re.compile("^t\d+")):
        tutorial = {attribute: None for attribute in ["title", "authors", "abstract", "datetime",
                                                      "location", "link"]}
        tutorial["title"] = pretty_title(item.text)
        tutorial["authors"] = item.findNext("p").text.replace(" and ", ", ").split(", ")
        next_node = item.findNext("p").findNext("p")
        abstract = ""
        while next_node.name == "p":
            abstract += next_node.text + " "
            next_node = next_node.findNext()
        tutorial["abstract"] = abstract[:-1]
        tutorials.append(tutorial)
        tutorial_reference[pretty_title(item.text).replace(" ", "").lower()] = reference_counter
        reference_counter += 1

    # gather and merge with information available in interactive schedule

    if schedule_url is None:
        return tutorials

    try:
        page = request.urlopen(schedule_url)
    except:
        print("Could not connect to url.")

    tutorial_sessions = BeautifulSoup(page, 'html.parser')\
        .findAll("div", {"class": "session session-expandable session-tutorials"})

    for session in tutorial_sessions:
        time = session.find("span", {"class" : "session-time"})
        datetime = time["title"] + ", " + time.text
        for child in session.findChildren("span", {"class": "tutorial-title"}):
            title = pretty_title(child.find("strong").text)
            location = child.findNext("span", {"class" : "btn"}).text
            try:
                goal_index = tutorial_reference[title.replace(" ", "").lower()]
                if tutorials[goal_index]["datetime"] is None:
                    tutorials[goal_index]["datetime"] = datetime
                    tutorials[goal_index]["location"] = location
                else:
                    cur_datetime = tutorials[goal_index]["datetime"] + ", " + time.text
                    tutorials[goal_index]["datetime"] = cur_datetime
            except KeyError:
                print("KeyException[ " + title + " ] not found in papers!")

    #print(json.dumps(tutorials, indent=1))
    return tutorials

def pretty_title(title_string):
    filter1 = re.sub(r'(\[\w+\]\s|\.\s*$|[\t\n’\“\”]|^T\d+:\s)', "", title_string)
    return filter1

