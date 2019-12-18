"""Crawler to collect the keynotes data"""
__author__ = "Lars Meister"

from bs4 import BeautifulSoup
from urllib import request
import re
from confcrawler.util.util import basic_string_clean
import logging

logger = logging.getLogger("keynote_crawler")


def extract_keynotes(keynotes_url=None, schedule_url=None):
    """
    Extracts basic information available for keynotes provided at
    the keynote site of the conference and extract and merge with data for a
    keynote if interactive schedule of conference is specified.
    One url of the the two must be provided. If only one is specified, the crawler tries to
    extract as much information as it can from this site. Its recommended to specify both urls,
    then the crawler extracts all available data starting with the keynote_url and afterwards
    merges the data with results of the crawled data from the schedule url.
    :param: keynotes_url: the url where the keynotes are listed (default None)
            (for example https://naacl2019.org/program/keynotes/ )
    :param: schedule_url: the url of the interactive schedule if available (default None)
            (for example: https://www.emnlp-ijcnlp2019.org/program/ischedule/ )
    :return: list of dictionaries with a keynote represented as one dictionary.
    """
    logger.info('Start crawling KEYNOTES...')
    keynotes = []

    keynote_reference = {}  # we need this dictionary to merge existing tutorials with the
    # schedule data

    # extract information from tutorial site
    if keynotes_url is not None:
        logger.info('Crawling data from: %s', keynotes_url)
        try:
            page = request.urlopen(keynotes_url)
        except:
            logger.warning("URl could not be crawled!")
            return keynotes

        soup = BeautifulSoup(page, 'html.parser').find("section", {"class": "page__content"})

        reference_counter = 0
        items = soup.find_all(class_="archive__item-body")

        for item in items:
            keynote = {attribute: None for attribute in ["title", "authors", "abstract", "datetime",
                                                          "location", "link", "author-bio"]}
            title_parent = item.find(class_="archive__item-excerpt").find("strong",
                                                    text=re.compile("^\s?[Tt]itle\s?:\s?"))
            abstract_parent = item.find(class_="archive__item-excerpt").find("strong",
                                                    text=re.compile("^\s?[Aa]bstract\s?:\s?"))
            author_bio = item.find(class_="archive__item-small-excerpt")
            if title_parent is not None:
                title = basic_string_clean(str(title_parent.next_sibling))
                keynote["title"] = title
                if abstract_parent is not None:
                    keynote["abstract"] = basic_string_clean(str(abstract_parent.next_sibling))
                if author_bio is not None:
                    keynote["author-bio"] = basic_string_clean(author_bio.text)

                keynotes.append(keynote)
                keynote_reference[clean_title(title)] = reference_counter
                reference_counter += 1

    if schedule_url is None:
        logger.info('Crawling DONE: no schedule url specified')
        return keynotes

    # extract information from tutorial site
    logger.info('Crawling data from: %s', schedule_url)
    try:
        page = request.urlopen(schedule_url)
    except Exception:
        logger.warning("URl could not be crawled!")

    plenary_sessions = BeautifulSoup(page, 'html.parser')\
        .findAll("div", {"class": "session session-expandable session-plenary"})

    for session in plenary_sessions:
        title = session.findNext("a", {"class": "session-title"}).text
        if title.startswith("Keynote"):
            search_title = clean_title(title)
            # if keynote exist already merge results
            if search_title in keynote_reference:
                logger.debug('Merge existing keynote: **%s', title)
                existing_index = keynote_reference[search_title]
                authors = session.find("span", {"class": "session-people"})
                if authors is None:
                    authors = session.find("span", {"class": "session-person"})
                keynotes[existing_index]["authors"] = authors.text
                time = session.find("span", {"class": "session-time"})
                keynotes[existing_index]["datetime"] = time["title"] + ", " + time.text
                keynotes[existing_index]["location"] = session.findNext("span", {"class": "btn"}).text

            # if keynote does not exist add new keynote
            else:
                logger.debug('Keynote does not exist already: Create new: *%s', title)
                keynote = {attribute: None for attribute in
                           ["title", "authors", "abstract", "datetime",
                            "location", "link", "author-bio"]}
                if title:
                    keynote["title"] = pretty_title(title)
                    authors = session.find("span", {"class": "session-people"})
                    if authors is None:
                        authors = session.find("span", {"class": "session-person"})
                    keynote["authors"] = authors.text
                    time_parent = session.find("span", {"class": "session-time"})
                    if time_parent is not None:
                        keynote["datetime"] = time_parent["title"] + ", " + time_parent.text
                    location_parent = session.findNext("span", {"class": "btn"})
                    if location_parent is not None:
                        keynote["location"] = location_parent.text
                    abstract_parent = session.findNext("div", {"class": "session-abstract"})
                    if abstract_parent is not None:
                        keynote["abstract"] = basic_string_clean(abstract_parent.text)
                    keynotes.append(keynote)
    logger.info('Crawling KEYNOTES DONE')
    return keynotes

def clean_title(title):
    filter1 = re.sub(r'(^\s?[Kk]eynote[\w\s]+:\s?|[\"\t\n]|\s)', "", title.lower())
    return filter1

def pretty_title(title):
    filter1 = re.sub(r'(^[\w\s]+:\s?|[\"\t\n])', "", title)
    return filter1
