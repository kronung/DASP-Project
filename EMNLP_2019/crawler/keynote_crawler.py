"""Crawler to collect the EMNLP 2019 keynotes from interactive schedule"""
__author__ = "Lars Meister"

from bs4 import BeautifulSoup
from urllib import request
import json


def extract_keynotes():
    """
    Extracts all information available for keynotes in the interactive schedule at
    https://www.emnlp-ijcnlp2019.org/program/ischedule/ .
    :return: list of dictionaries with a keynote represented as one dictionary.
    """
    keynotes = []
    url = "https://www.emnlp-ijcnlp2019.org/program/ischedule/"

    try:
        page = request.urlopen(url)
    except:
        print("Could not connect to url.")

    plenary_sessions = BeautifulSoup(page, 'html.parser')\
        .findAll("div", {"class": "session session-expandable session-plenary"})

    for session in plenary_sessions:
        title = session.findNext("a", {"class": "session-title"}).text
        if title.startswith("Keynote"):
            keynote = {attribute: None for attribute in ["title", "authors", "abstract",
                                                         "datetime","location", "link"]}
            keynote["title"] = title.split(": ")[1].replace("\"", "")
            keynote["authors"] = session.find("span", {"class": "session-people"}).text
            time = session.find("span", {"class": "session-time"})
            keynote["datetime"] = time["title"] + ", " + time.text
            keynote["location"] = session.findNext("span", {"class": "btn"}).text
            keynote["abstract"] = session.findNext("div", {"class": "session-abstract"}).text
            keynotes.append(keynote)

    #print(json.dumps(keynotes, indent=1))
    return keynotes