"""Crawler to collect the EMNLP 2019 keynotes from interactive schedule"""
__author__ = "Lars Meister"

from bs4 import BeautifulSoup
from urllib import request
import json
import re


def extract_keynotes(schedule_url):
    """
    Extracts all information available for keynotes in the interactive schedule at
    https://www.emnlp-ijcnlp2019.org/program/ischedule/ .
    :return: list of dictionaries with a keynote represented as one dictionary.
    """
    keynotes = []
    #url = "https://www.emnlp-ijcnlp2019.org/program/ischedule/"

    try:
        page = request.urlopen(schedule_url)
    except:
        print("Could not connect to url.")

    plenary_sessions = BeautifulSoup(page, 'html.parser')\
        .findAll("div", {"class": "session session-expandable session-plenary"})

    for session in plenary_sessions:
        title = session.findNext("a", {"class": "session-title"}).text
        if title.startswith("Keynote"):
            keynote = {attribute: None for attribute in ["title", "authors", "abstract",
                                                         "datetime","location", "link"]}
            keynote["title"] = clean_keynote_title(title)
            authors = session.find("span", {"class": "session-people"})
            if authors is None:
                authors = session.find("span", {"class": "session-person"})
            keynote["authors"] = authors.text
            time = session.find("span", {"class": "session-time"})
            keynote["datetime"] = time["title"] + ", " + time.text
            keynote["location"] = session.findNext("span", {"class": "btn"}).text
            keynote["abstract"] = session.findNext("div", {"class": "session-abstract"}).text
            keynotes.append(keynote)

    #print(json.dumps(keynotes, indent=1))
    return keynotes

def clean_keynote_title(title):
    filter1 = re.sub(r'(^[\w\s]+:\s?|[\"\t\n])', "", title)
    return filter1