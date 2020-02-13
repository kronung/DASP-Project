__author__ = "Aron Kaufmann"
import copy
from urllib import request
from bs4 import BeautifulSoup

from confcrawler.util import util


def get_timestamps(url):
    try:
        page = request.urlopen(url)
    except ConnectionError:
        print("Could not connect to url.")
    timestamps = BeautifulSoup(page, 'html.parser').findAll("h2", {"class": "tutorials-anchor"})
    time_tuple_list = []
    for time in timestamps:
        time_tuple_list.append((time.text, time.findNext("h3", class_="tutorials-anchor").text))
    return time_tuple_list


def extract_tutorial_info(url):
    tutorial_dummy = {attribute: None for attribute in ["tutorial_name", "tutorial_author", "tutorial_abstract", "tutorial_time",
                                                          "tutorial_location", "tutorial_link"]}
    tutorial_info_list = []
    try:
        page = request.urlopen(url)
    except ConnectionError:
        print("Could not connect to url.")

    datetimes = get_timestamps(url)
    tutorials = BeautifulSoup(page, 'html.parser').findAll("h3", {"class": "tutorials-anchor"})
    for tutorial in tutorials:
        tutorial_dummy["tutorial_name"] = util.basic_string_clean(tutorial.text)
        if tutorial.text[:2] < datetimes[1][1][:2]:
            tutorial_dummy["tutorial_time"] = datetimes[0][0]
        elif tutorial.text[:2] >= datetimes[1][1][:2]:
            tutorial_dummy["tutorial_time"] = datetimes[1][0]
        next = tutorial.findNext("div")
        tutorial_dummy["tutorial_author"] = tutorial.findNext("p", {"class": "tutorials-tutors"}).text
        tutorial_dummy["tutorial_location"] = tutorial.findNext("p", {"class": "tutorials-room"}).text.split('.')[1].strip()
        tutorial_dummy["tutorial_link"] = tutorial.findNext("a", {"class": "tutorials-materials"})["href"]
        abstract_p = next.findAll("p", class_=None)
        abstract = ""
        for p in abstract_p:
            abstract += p.text
        tutorial_dummy["abstract"] = abstract
        tutorial_info_list.append(copy.copy(tutorial_dummy))
    return tutorial_info_list


def get_tutorials():
    tutorials_info = extract_tutorial_info("http://www.acl2019.org/EN/tutorials.xhtml")
    # for t in tutorials_info:
    #     print(t)
    return tutorials_info

