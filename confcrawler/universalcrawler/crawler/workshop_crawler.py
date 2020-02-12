"""Crawler to collect the workshops data"""
__author__ = "Lars Meister"

from bs4 import BeautifulSoup
from urllib import request
from re import sub
import logging
from confcrawler.util.util import basic_string_clean

logger = logging.getLogger("workshop_crawler")

def extract_workshops(workshops_url=None, schedule_url=None):
    """
    Extracts basic information available for workshops provided at
    the workshop site of the conference and extract and merge with data for a
    workshop if interactive schedule of conference is specified.
    One url of the the two must be provided. If only one is specified, the crawler tries to
    extract as much information as it can from this site. Its recommended to specify both urls,
    then the crawler extracts all available data starting with the workshops_url and afterwards
    merges the data with results of the crawled data from the schedule url.
    :param: tutorials_url: the url where the workshops are listed (default None)
            (for example https://www.emnlp-ijcnlp2019.org/program/workshops/ )
    :param: schedule_url: the url of the interactive schedule if available (default None)
            (for example: https://www.emnlp-ijcnlp2019.org/program/ischedule/ )
    :return: list of dictionaries with a workshop represented as one dictionary.
    """
    logger.info('Start crawling WORKSHOPS...')
    workshops = []
    workshop_reference = {} # we need this dictionary to merge existing workshops with the
                            # schedule data

    if workshops_url is not None:
        logger.info('Crawling data from: %s', workshops_url)
        # extract information from workshop site
        try:
            page = request.urlopen(workshops_url)
        except:
            logger.warning("URl could not be crawled!")
            return workshops

        soup = BeautifulSoup(page, 'html.parser').find("section", {"class": "page__content"})

        reference_counter = 0

        # Cases
        for child in soup.findChildren("h3"):
            workshop = {attribute: None for attribute in ["workshop_name", "workshop_organizer", "workshop_description", "workshop_day",
                                                               "workshop_location", "workshop_link"]}
            workshop["workshop_name"] = pretty_title(child.text)
            next_node = child
            abstract = ""

            for tag in next_node.next_elements:
                if tag.name in ["h2", "h3", "footer"]:
                    break
                elif tag.name in ["p", "div", "ul"]:
                    abstract += tag.text
                elif tag.name == "a":
                    workshop["workshop_link"] = tag["href"]
                elif tag.name == "em":
                    workshop["workshop_organizer"] = clean_organizers(tag.text)

            workshop["workshop_description"] = basic_string_clean(abstract)
            workshops.append(workshop)
            workshop_reference[clean_title(child.text)] = reference_counter
            reference_counter += 1

    #url = "https://www.emnlp-ijcnlp2019.org/program/ischedule/"

    # gather and merge with information available in interactive schedule
    if schedule_url is None:
        logger.info('Crawling DONE: no schedule url specified')
        return workshops

    logger.info('Crawling data from: %s', schedule_url)
    try:
        page = request.urlopen(schedule_url)
    except:
        logger.warning("URl could not be crawled!")
        return workshops

    workshop_sessions = BeautifulSoup(page, 'html.parser')\
        .findAll(class_="session-workshops")

    for session in workshop_sessions:
        date = session.find(class_="session-time")["title"]
        for child in session.findChildren(class_="workshop-title"):
            title = child.find("strong").text
            search_title = clean_title(title)

            # if workshop already exists merge
            if search_title in workshop_reference:
                logger.debug('Merge existing workshop: **%s', title)
                existing_index = workshop_reference[search_title]
                time_parent = child.findNext("span", {"class" : "session-time"})
                if time_parent is not None:
                    time = time_parent.text
                else:
                    time = child.find("strong").next_sibling.strip()
                location_parent = child.findNext(class_="btn")
                if location_parent is not None:
                    workshops[existing_index]["workshop_location"] = location_parent.text
                    workshops[existing_index]["workshop_day"] = date + ", " + time

            # if workshop does not exist add to tutorials
            else:
                logger.debug('Workshop does not exist already: Create new: *%s', title)
                workshop = {attribute: None for attribute in
                            ["workshop_name", "workshop_organizer", "workshop_description", "workshop_day",
                             "workshop_location", "workshop_link"]}
                workshop["workshop_name"] = pretty_title(title)
                time_parent = child.findNext("span", {"class": "session-time"})
                if time_parent is not None:
                    time = time_parent.text
                else:
                    time = child.find("strong").next_sibling.strip()
                location_parent = child.findNext(class_="btn")
                if location_parent is not None:
                    workshops["workshop_location"] = location_parent.text
                    workshops["workshop_day"] = date + ", " + time
                workshops.append(workshop)

    logger.info('Crawling WORKSHOPS DONE')
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