__author__ = "Aron Kaufmann"

import copy
from urllib import request
from bs4 import BeautifulSoup
from bs4 import element

from confcrawler.util import util


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


def extract_workshop_info(url):
    workshop_dummy = {attribute: None for attribute in
                      ["workshop_name", "workshop_organizer", "workshop_description", "workshop_day",
                       "workshop_location", "workshop_link"]}
    workshop_info_list = []
    try:
        page = request.urlopen(url)
    except ConnectionError:
        print("Could not connect to url.")

    datetimes = get_timestamps(url)
    current_date = datetimes[0][0]
    workshop_div = BeautifulSoup(page, 'html.parser').findAll("div", class_="workshops")[0]
    workshops = workshop_div.findAll("h3")
    for workshop in workshops:
        workshop_dummy["workshop_name"] = util.basic_string_clean(workshop.text)
        current_date = get_timestamp_for_event(datetimes, (current_date, workshop.text))
        workshop_dummy["workshop_day"] = current_date
        workshop_dummy["workshop_link"] = workshop.contents[0]["href"]
        workshop_dummy["workshop_organizer"] = util.basic_string_clean(workshop.findNext("p", {"class": "tutorials-tutors"}).text)
        workshop_dummy["workshop_location"] = workshop.findNext("p", {"class": "tutorials-room"}).text.split('.')[
            1].strip()
        workshop_info_list.append(copy.copy(workshop_dummy))
    return workshop_info_list


def get_workshops():
    workshop_info = extract_workshop_info("http://www.acl2019.org/EN/workshops.xhtml")
    # for t in workshop_info:
    #     print(t)
    return workshop_info
