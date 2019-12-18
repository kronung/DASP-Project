"""Crawler to collect the EMNLP 2019 papers"""
__author__ = "Lars Meister"

from bs4 import BeautifulSoup
from urllib import request
import re
import json
import logging

logger = logging.getLogger("paper_crawler")

def extract_papers(papers_url=None, schedule_url=None):
    """
    Extracts basic information available for papers provided at
    the papers site of the conference and extract and merge with data for a
    paper if interactive schedule of conference is specified.
    One url of the the two must be provided. If only one is specified, the crawler tries to
    extract as much information as it can from this site. Its recommended to specify both urls,
    then the crawler extracts all available data starting with the papers_url and afterwards
    merges the data with results of the crawled data from the schedule url.
    :param: papers_url: the url where the papers are listed (default None)
            (for example https://naacl2019.org/program/accepted/ )
    :param: schedule_url: the url of the interactive schedule if available (default None)
            (for example: https://www.emnlp-ijcnlp2019.org/program/ischedule/ )
    :return: list of dictionaries with a papers represented as one dictionary.
    """
    logger.info('Start crawling PAPERS...')
    papers = []
    paper_reference = {}
    author_reference =[]

    # crawl the papers site

    if papers_url is not None:
        logger.info('Crawling data from: %s', papers_url)
        try:
            page = request.urlopen(papers_url)
        except:
            logger.warning("URl could not be crawled!")
            return papers

        soup = BeautifulSoup(page, 'html.parser').find("section", {"class": "page__content"})

        reference_counter = 0

        # on the accepted papers site, papers can either be in <ul> tags or just be <p> tags
        content_determine = soup.findNext("h2").find_next_sibling("p")

        # if papers are just <p> tags
        if content_determine is not None:
            logger.debug('Content tag where data is in: <p>')

            for paper_entry in soup.findAll("p"):
                paper = {attribute: None for attribute in ["title", "authors", "type", "link",
                                                                   "datetime", "topic"]}
                paper_parent = paper_entry.strong
                if paper_parent is not None:
                    paper["title"] = pretty_title(paper_parent.text)
                    author_parent = paper_parent.next_sibling
                    if author_parent is not None:
                        paper["authors"] = pretty_organizers(author_parent.next)
                        author_reference.append(
                            set(clean_authors(author_parent.next)))
                    papers.append(paper)
                    paper_reference[clean_title(paper_entry.strong.text)] = reference_counter
                    reference_counter += 1

        # if papers are in table <ul> <li>
        else:
            logger.debug('Content tag where data is in: <li>')
            for child in soup.findAll("h2"):
                paper_type = child.text
                for paper_entry in child.findNext('ul').findChildren("li"):
                    paper = {attribute: None for attribute in ["title", "authors", "type", "link",
                                                               "datetime", "topic"]}
                    paper["type"] = paper_type
                    paper_parent = paper_entry.span
                    if paper_parent is not None:
                        paper["title"] = pretty_title(paper_parent.text)
                        author_parent = paper_entry.i
                        if author_parent is not None:
                            paper["authors"] = pretty_organizers(author_parent.text)
                            author_reference.append(set(clean_authors(author_parent.text)))
                        papers.append(paper)
                        paper_reference[clean_title(paper_parent.text)] = \
                            reference_counter
                        reference_counter += 1

    # crawl the schedule site and merge results
    # try to extract link, datetime and category topics and merge with existing papers
    #url = "https://www.emnlp-ijcnlp2019.org/program/ischedule/"

    if schedule_url is None:
        logger.info('Crawling DONE: no schedule url specified')
        return papers

    logger.info('Crawling data from: %s', schedule_url)
    try:
        page = request.urlopen(schedule_url)
    except:
        print("Could not connect to url.")

    paper_sessions = BeautifulSoup(page, 'html.parser') \
        .findAll("div", {"class": "session-box"})

    for session in paper_sessions:
        for box in session.findChildren("div", {"class": "session"}):
            box_type = "paper"
            topic = ""
            topic_parent = box.find("a", {"class": "session-title"})
            if topic_parent is not None:
                topic = topic_parent.text.split(": ")[1]
            time = box.find("span", {"class": "session-time"})
            datetime = ""
            if time is not None:
                datetime = time["title"] + ", " + time.text
            # session poster
            if box.get("class")[2] == "session-posters":
                box_type = "poster"
            for paper in box.findChildren("tr", {"id": box_type}):
                title_parent = paper.find("span", {"class": box_type + "-title"})
                if title_parent is not None:
                    title = paper.find("span", {"class": box_type + "-title"}).text[:-2]
                    authors_parent = paper.find('em')
                    search_authors = set()
                    authors = ""
                    if authors_parent is not None:
                        authors = authors_parent.text
                        search_authors = set(clean_authors(authors))

                    search_title = clean_title(title)

                    # if paper exist already merge results
                    if (search_title in paper_reference) or (search_authors in author_reference):
                        logger.debug('Merge existing paper: **%s', title)
                        try:
                            existing_index = paper_reference[search_title]
                        except KeyError:
                            existing_index = author_reference.index(search_authors)

                        papers[existing_index]["datetime"] = datetime
                        papers[existing_index]["topic"] = topic
                        link_parent = paper.find('i')
                        if link_parent is not None:
                            papers[existing_index]["link"] = link_parent['data']

                    # if paper does not exist add new keynote
                    else:
                        logger.debug('Paper does not exist already: Create new: *%s', title)
                        paper_ = {attribute: None for attribute in ["title", "authors", "type",
                                                                    "link",
                                                                   "datetime", "topic"]}
                        paper_["title"] = pretty_title(title)
                        paper_["authors"] = pretty_organizers(authors)
                        paper_["topic"] = topic
                        link_parent = paper.find('i')
                        if link_parent is not None:
                            paper_["link"] = link_parent['data']
                        paper_["datetime"] = datetime
                        papers.append(paper_)

    logger.info('Crawling PAPERS DONE')
    return papers

def clean_title(title):
    filter1 = re.sub(r'(^#[0-9]*:|\[\w+\]|\.$|[\t\n\'\"’\s\“\”])', "", title.lower())
    return filter1
def clean_authors(authors_string):
    filter1 = re.sub(r'([\t\n\'\"’\s\.])', "", authors_string.lower()
                     .replace(", and ", ", """).replace(" and ", ", "))
    return filter1.split(",")

def pretty_title(title):
    filter1 = re.sub(r'([\t\n]|^#\d+:\s?)', "", title)
    return filter1

def pretty_organizers(organizers_string):
    filter1 = re.sub(r'(^[\w\s]+:\s?|\s?[\w\s-]+:|\.*\s*$|^[\n\t\s]*)', "", organizers_string)
    return filter1.replace(", and ", ", ").replace(" and ", ", ").split(", ")
