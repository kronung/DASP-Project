"""Crawler to collect the EMNLP 2019 workshops"""
__author__ = "Lars Meister"

from bs4 import BeautifulSoup
from urllib import request
import json


def extract_workshops():
    """
    Extracts all information available for workshops provided at
    https://www.emnlp-ijcnlp2019.org/program/workshops/ and
    https://www.emnlp-ijcnlp2019.org/program/ischedule/
    :return: list of dictionaries with a workshop represented as one dictionary.
    """
    workshops = []
    workshop_reference = {}
    url = "https://www.emnlp-ijcnlp2019.org/program/workshops/"

    try:
        page = request.urlopen(url)
    except:
        print("Could not connect to url.")

    soup = BeautifulSoup(page, 'html.parser').find("section", {"class": "page__content"})

    reference_counter = 0
    for child in soup.findChildren("h3"):
        workshop = {attribute: None for attribute in ["title", "authors", "abstract", "datetime",
                                                           "location", "link"]}
        workshop["title"] = child.text.split(" (")[0] + " " + child.findNext("p").find("a").text
        workshop["abstract"] = child.findNext("p").text.replace('\n','')
        workshop["link"] = child.findNext("p").find("a")["href"]
        workshops.append(workshop)
        workshop_reference[child.text.split(" (")[0]] = reference_counter
        reference_counter += 1

    url = "https://www.emnlp-ijcnlp2019.org/program/ischedule/"

    try:
        page = request.urlopen(url)
    except:
        print("Could not connect to url.")

    workshop_sessions = BeautifulSoup(page, 'html.parser')\
        .findAll("div", {"class": "session session-expandable session-workshops"})

    for session in workshop_sessions:
        date = session.find("span", {"class" : "session-time"})["title"]
        for child in session.findChildren("span", {"class": "workshop-title"}):
            title = child.find("strong").text.split(":")[0]
            if (child.findNext("span", {"class" : "session-time"}) is not None):
                time = child.findNext("span", {"class" : "session-time"}).text
            else:
                time = child.find("strong").next_sibling.strip()
            location = child.findNext("span", {"class" : "btn"}).text
            goal_index = workshop_reference[title]
            workshops[goal_index]["datetime"] = date + ", " + time
            workshops[goal_index]["location"] = location

    print(json.dumps(workshops, indent=1))
    return workshops