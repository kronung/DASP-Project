"""Crawler to collect the EMNLP 2019 papers"""
__author__ = "Lars Meister"

from bs4 import BeautifulSoup
from urllib import request
import re
import json


def extract_papers(papers_url, schedule_url=None):
    """
    Extracts all information available for papers provided at
    https://www.emnlp-ijcnlp2019.org/program/accepted/ and
    https://www.emnlp-ijcnlp2019.org/program/ischedule/
    :return: list of dictionaries with a paper represented as one dictionary.
    """
    papers = []
    paper_reference = {}
    author_reference =[]

    # crawl the papers site
    # extract title, authors and group for each paper
    #url = "https://www.emnlp-ijcnlp2019.org/program/accepted/"

    try:
        page = request.urlopen(papers_url)
    except:
        print("Could not connect to url.")

    soup = BeautifulSoup(page, 'html.parser').find("section", {"class": "page__content"})

    reference_counter = 0

    # on the accepted papers site, papers can either be in <ul> tags or just be <p> tags
    content_determine = soup.findNext("h2").find_next_sibling("p")

    # if papers are just <p> tags
    if content_determine is not None:

        for paper_entry in soup.findAll("p"):
            paper = {attribute: None for attribute in ["title", "authors", "type", "link",
                                                               "datetime", "topic"]}
            paper["title"] = paper_entry.strong.text.replace("\t", "")
            paper["authors"] = paper_entry.strong.next_sibling.next.replace(' and ', ', ')\
                .replace("\t","").replace("\n", "").split(', ')
            papers.append(paper)
            paper_reference[clean_title(paper_entry.strong.text)] = reference_counter
            author_reference.append(set(clean_authors(paper_entry.strong.next_sibling.next)))
            reference_counter += 1

    # if papers are in table <ul> <li>
    else:
        for child in soup.findAll("h2"):
            #filter_tag =
            #if child.find_next_sibling("p") is not None:
            #    paper_content = child.find('p')
            paper_type = child.text
            for paper_entry in child.findNext('ul').findChildren("li"):
                paper = {attribute: None for attribute in ["title", "authors", "type", "link",
                                                           "datetime", "topic"]}
                paper["type"] = paper_type
                paper["title"] = paper_entry.span.text.replace("\t", "")
                paper["authors"] = paper_entry.i.text.replace(' and ', ', ').replace("\t", "").split(
                    ', ')
                papers.append(paper)
                paper_reference[clean_title(paper_entry.span.text)] = \
                    reference_counter
                author_reference.append(set(clean_authors(paper_entry.i.text)))
                reference_counter += 1

    # crawl the schedule site and merge results
    # try to extract link, datetime and category topics and merge with existing papers
    #url = "https://www.emnlp-ijcnlp2019.org/program/ischedule/"

    if schedule_url is None:
        return papers

    try:
        page = request.urlopen(schedule_url)
    except:
        print("Could not connect to url.")

    paper_sessions = BeautifulSoup(page, 'html.parser') \
        .findAll("div", {"class": "session-box"})

    for session in paper_sessions:
        for box in session.findChildren("div", {"class": "session"}):
            box_type = "paper"
            topic = box.find("a", {"class": "session-title"}).text.split(": ")[1]
            time = box.find("span", {"class": "session-time"})
            datetime = time["title"] + ", " + time.text
            # session poster
            if box.get("class")[2] == "session-posters":
                box_type = "poster"
            for paper in box.findChildren("tr", {"id": box_type}):
                title = paper.find("span", {"class": box_type + "-title"}).text[:-2]
                try:
                    goal_index = paper_reference[clean_title(title)]
                    papers[goal_index]["datetime"] = datetime
                    papers[goal_index]["topic"] = topic
                    papers[goal_index]["link"] = paper.find("i")['data']
                except KeyError:
                    try:
                        authors = set(clean_authors(paper.find("em").text))
                        goal_index = author_reference.index(authors)
                        papers[goal_index]["datetime"] = datetime
                        papers[goal_index]["topic"] = topic
                        papers[goal_index]["link"] = paper.find("i")['data']
                    except KeyError:
                        print("KeyException[ " + title + " ] not found in papers!")
                    except ValueError:
                        print("KeyException[ " + title + " && " + str(authors) +"] not found "
                                                                                "in papers authors!")

    #print(paper_reference)
    #print(json.dumps(papers, indent=1))
    return papers

def clean_title(title):
    filter1 = re.sub(r'(^#[0-9]*:|\[\w+\]|\.$|[\t\n\'\"’\s\“\”])', "", title.lower())
    return filter1
def clean_authors(authors_string):
    filter1 = re.sub(r'([\t\n\'\"’\s\.])', "", authors_string.lower()
                     .replace(", and ", ", """).replace(" and ", ", "))
    return filter1.split(",")
