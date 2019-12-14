"""Crawler to collect the EMNLP 2019 workshops"""
__author__ = "Lars Meister"

from bs4 import BeautifulSoup
from urllib import request
from json import dumps
from re import sub
from util import basic_string_clean


def extract_workshops(workshops_url, schedule_url=None):
    """
    Extracts basic information available for workshops provided at
    the workshop site of the conference and tries to extract and merge with optional data for a
    workshop if interactive schedule of conference is specified.
    :param: workshops_url: the url where the workshops are listed
            (for example https://naacl2019.org/program/workshops/ ,
                         https://www.emnlp-ijcnlp2019.org/program/workshops/ )
    :param: schedule_url: the url of the interactive schedule if available (default None)
            (for example: https://www.emnlp-ijcnlp2019.org/program/ischedule/ )
    :return: list of dictionaries with a workshop represented as one dictionary.
    """
    workshops = []
    workshop_reference = {} # we need this dictionary to merge existing workshops with the
                            # schedule data

    # extract information from workshop site
    try:
        page = request.urlopen(workshops_url)
    except:
        print("Could not connect to url.")

    soup = BeautifulSoup(page, 'html.parser').find("section", {"class": "page__content"})

    reference_counter = 0
    for child in soup.findChildren("h3"):
        workshop = {attribute: None for attribute in ["title", "authors", "abstract", "datetime",
                                                           "location", "link"]}
        workshop["title"] = pretty_title(child.text)
        workshop["abstract"] = basic_string_clean(child.findNext("p").text)
        organizers = child.findNext("em")
        if organizers is not None:
            workshop["authors"] = clean_organizers(organizers.text)
        link = child.findNext("p").find("a")
        if link is not None:
            workshop["link"] = link["href"]
        workshops.append(workshop)
        workshop_reference[clean_title(child.text)] = reference_counter
        reference_counter += 1

    #url = "https://www.emnlp-ijcnlp2019.org/program/ischedule/"

    # gather and merge with information available in interactive schedule
    if schedule_url is None:
        return workshops
    try:
        page = request.urlopen(schedule_url)
    except:
        print("Could not connect to url.")

    workshop_sessions = BeautifulSoup(page, 'html.parser')\
        .findAll("div", {"class": "session session-expandable session-workshops"})

    for session in workshop_sessions:
        date = session.find("span", {"class" : "session-time"})["title"]
        for child in session.findChildren("span", {"class": "workshop-title"}):
            title = clean_title(child.find("strong").text)
            if (child.findNext("span", {"class" : "session-time"}) is not None):
                time = child.findNext("span", {"class" : "session-time"}).text
            else:
                time = child.find("strong").next_sibling.strip()
            location = child.findNext("span", {"class" : "btn"}).text
            try:
                goal_index = workshop_reference[title]
                workshops[goal_index]["datetime"] = date + ", " + time
                workshops[goal_index]["location"] = location
            except KeyError:
                print("KeyException[ " + title + " ] not found in schedule!")

    #print(dumps(workshops, indent=1))
    return workshops

def clean_organizers(organizers_string):
    filter1 = sub(r'(^[\w\s]+:\s?|\s?[\w\s-]+:)', "", organizers_string)
    return filter1.replace(", and ", ", ").replace(" and ", ", ").split(", ")

def pretty_title(title):
    filter1 = sub(r'(^\s?\[\w+\]\s?|\s?\([\w\s]+\)\s?$|\.$)', "", title)
    return filter1

def clean_title(title):
    filter1 = sub(r'(^\s?\[\w+\]\s?|\s?\([\w\s]+\)\s?|\.$|\s)', "", title.lower())
    try:
        filter2 = filter1.split(":")[0]
    except KeyError:
        return filter1
    return filter2
