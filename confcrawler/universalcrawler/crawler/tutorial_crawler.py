"""Crawler to collect tutorial data"""
__author__ = "Lars Meister"

from bs4 import BeautifulSoup
from urllib import request
import re
import logging
from confcrawler.util.util import basic_string_clean

logger = logging.getLogger("tutorial_crawler")

def extract_tutorials(tutorials_url=None, schedule_url=None):
    """
    Extracts basic information available for tutorials provided at
    the tutorial site of the conference and extract and merge with data for a
    tutorial if interactive schedule of conference is specified.
    One url of the the two must be provided. If only one is specified, the crawler tries to
    extract as much information as it can from this site. Its recommended to specify both urls,
    then the crawler extracts all available data starting with the tutorials_url and afterwards
    merges the data with results of the crawled data from the schedule url.
    :param: tutorials_url: the url where the tutorials are listed (default None)
            (for example https://www.emnlp-ijcnlp2019.org/program/tutorials/ )
    :param: schedule_url: the url of the interactive schedule if available (default None)
            (for example: https://www.emnlp-ijcnlp2019.org/program/ischedule/ )
    :return: list of dictionaries with a tutorial represented as one dictionary.
    """
    logger.info('Start crawling TUTORIALS...')
    tutorials = []
    tutorial_reference = {} # we need this dictionary to merge existing tutorials with the
                            # schedule data
    author_reference = []

    if tutorials_url is not None:
        logger.info('Crawling data from: %s', tutorials_url)
        # extract information from tutorial site
        try:
            page = request.urlopen(tutorials_url)
        except:
            logger.warning("URl could not be crawled!")
            return tutorials

        soup = BeautifulSoup(page, 'html.parser').find("section", {"class": "page__content"})

        reference_counter = 0
        # tutorials can either be in <h2> or <h3> tags
        for item in soup.find_all(['h2', 'h3'], id= re.compile("^t\d+")):
            tutorial = {attribute: None for attribute in ["title", "authors", "abstract", "datetime",
                                                          "location", "link"]}
            tutorial["title"] = pretty_title(item.text)
            tutorial["authors"] = pretty_organizers(item.findNext("p").text)
            next_node = item.findNext("p")
            tagbreak = item.name
            abstract = ""
            for tag in next_node.next_siblings:
                if tag.name == tagbreak:
                    break
                elif tag.name in ["p", "div", "ul"]:
                    abstract += tag.text
            tutorial["abstract"] = basic_string_clean(abstract)
            tutorials.append(tutorial)
            tutorial_reference[clean_title(item.text)] = reference_counter
            author_reference.append(set(clean_authors(item.findNext("p").text)))
            reference_counter += 1

    # gather and merge with information available in interactive schedule

    if schedule_url is None:
        logger.info('Crawling DONE: no schedule url specified')
        return tutorials

    logger.info('Crawling data from: %s', schedule_url)
    try:
        page = request.urlopen(schedule_url)
    except:
        logger.warning("URl could not be crawled!")
        return tutorials

    tutorial_sessions = BeautifulSoup(page, 'html.parser')\
        .findAll("div", {"class": "session session-expandable session-tutorials"})
    for session in tutorial_sessions:
        time = session.find("span", {"class" : "session-time"})
        datetime = ""
        if time is not None:
            datetime = time["title"] + ", " + time.text
        for child in session.findChildren(class_="tutorial-title"):
            title_parent = child.find("strong")
            if title_parent is not None:
                title = title_parent.text
                authors_parent = title_parent.next_sibling
                if authors_parent is not None:
                    authors = str(authors_parent)

                    # if tutorial already exists merge
                    search_title = clean_title(title)
                    search_authors = clean_authors(authors)
                    if (search_title in tutorial_reference) or (search_authors in author_reference):
                        logger.debug('Merge existing tutorial: **%s', title)
                        try:
                            existing_index = tutorial_reference[search_title]
                        except KeyError:
                            existing_index = author_reference.index(search_authors)
                        location_parent = child.findNext(class_="btn")
                        location = None
                        if location_parent is not None:
                            location = location_parent.text
                        if tutorials[existing_index]["datetime"] is None:
                            tutorials[existing_index]["datetime"] = datetime
                            tutorials[existing_index]["location"] = location
                        else:
                            cur_datetime = tutorials[existing_index]["datetime"] + ", " + time.text
                            tutorials[existing_index]["datetime"] = cur_datetime

                    # if tutorial does not exist add to tutorials
                    else:
                        logger.debug('Tutorial does not exist already: Create new: *%s', title)
                        tutorial = {attribute: None for attribute in
                                    ["title", "authors", "abstract", "datetime",
                                     "location", "link"]}
                        tutorial["title"] = pretty_title(title)
                        tutorial["authors"] = pretty_organizers(authors)

                        location_parent = child.findNext(class_="btn")
                        if location_parent is not None:
                            tutorial["location"] = location_parent.text
                        tutorial["datetime"] = datetime
                        tutorials.append(tutorial)
    logger.info('Crawling TUTORIALS DONE')
    return tutorials

def pretty_title(title_string):
    filter1 = re.sub(r'(\[\w+\]\s|\.\s*$|[\t\n’\“\”]|^T\d+:\s|\s?\([\w\s-]+\)\s?\.?\s?$)', "",
                     title_string)
    return filter1

def clean_title(title_string):
    filter1 = re.sub(r'(\[\w+\]\s|\.\s*$|[\t\n’\“\”]|^[tT]\w*\d+:\s?|\s?\([\w\s-]+\)\s?\.?$|\s)', "",
                     title_string.lower())
    return filter1

def pretty_organizers(organizers_string):
    filter1 = re.sub(r'(^[\w\s]+:\s?|\s?[\w\s-]+:|\.*\s*$)', "", organizers_string)
    return filter1.replace(", and ", ", ").replace(" and ", ", ").split(", ")

def clean_authors(string):
    filter1 = re.sub(r'(^[\w\s]+:\s?|\s?[\w\s-]+:|\s|\.\s*$|\.)', "", string.lower()
                     .replace(", and ", ",""").replace(" and ", ","))
    return filter1.split(",")
