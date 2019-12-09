__author__ = "Aron Kaufmann"
import copy
from urllib import request
from bs4 import BeautifulSoup
from bs4 import element


def get_timestamps(url):
    try:
        page = request.urlopen(url)
    except ConnectionError:
        print("Could not connect to url.")
    timestamps = BeautifulSoup(page, 'html.parser').findAll("h2", {"class": "tutorials-anchor"})
    time_tuple_list = []
    for time in timestamps[1:]:
        time_tuple_list.append((time.text, time.findNext("h3").text))
    return time_tuple_list


def get_timestamp_for_event(datetimes, date_tuple):
    rdate = ""
    for date in datetimes:
        if date_tuple[1] == date[1]:
            rdate = date[0]
            break
        else:
            rdate = date_tuple[0]
    return rdate


def extract_tutorial_info(url):
    tutorial_dummy = {attribute: None for attribute in ["title", "authors", "location", "link"]}
    tutorial_info_list = []
    try:
        page = request.urlopen(url)
    except ConnectionError:
        print("Could not connect to url.")

    datetimes = get_timestamps(url)
    current_date = datetimes[0][0]
    workshop_div = BeautifulSoup(page, 'html.parser').findAll("div", class_="workshops")[0]
    workshops = workshop_div.findAll("h3")
    for workshop in workshops:
        tutorial_dummy["title"] = workshop.text
        current_date = get_timestamp_for_event(datetimes, (current_date, workshop.text))
        tutorial_dummy["datetime"] = current_date
        tutorial_dummy["link"] = workshop.contents[0]["href"]
        tutorial_dummy["authors"] = workshop.findNext("p", {"class": "tutorials-tutors"}).text
        tutorial_dummy["location"] = workshop.findNext("p", {"class": "tutorials-room"}).text.split('.')[1].strip()
        tutorial_info_list.append(copy.copy(tutorial_dummy))
    return tutorial_info_list


tutorials_info = extract_tutorial_info("http://www.acl2019.org/EN/workshops.xhtml")
for t in tutorials_info:
    print(t)
