"""Crawler to collect the EMNLP 2019 conference schedule"""
__author__ = "Lars Meister"

from bs4 import BeautifulSoup
from urllib import request
import json


url = "https://www.emnlp-ijcnlp2019.org/program/ischedule/"

try:
    page = request.urlopen(url)
except:
    print("Could not connect to url.")

soup = BeautifulSoup(page, 'html.parser').find("div", {"class": "schedule"})
schedule = soup.findChildren("div", recursive=False)

conference = {}
current_day = ""
sessions = []
data_collected = False

for child in schedule:
    classes = child.get("class")

    # new conference day
    if classes[0] == "day":
        if data_collected:
            conference[current_day] = sessions

        conference[child.getText()] = {}
        current_day = child.getText()
        sessions = []
        data_collected = True

    # session of a conference day
    elif classes[0] == "session":

        # session expandable
        if classes[1] == "session-expandable":
            session = {}
            session["session_title"] = child.find("a", {"class": "session-title"}).get_text()
            session["session_time"] = child.find("span", {"class": "session-time"}).get_text()

            if classes[2] == "session-plenary":
                people = child.find("span", {"class": "session-people"})
                if people is not None:
                    session["session_people"] = people.find("a").getText()
                more_details = child.find("div", {"class": "paper-session-details"})
                if more_details is not None:
                    session["session_abstract"] = child.find("div", {"class": "session-abstract"}).getText()

            # session tutorial
            elif classes[2] == "session-tutorials":
                tutorials = []
                for cur_tutorial in child.findChildren("span", {"class": "tutorial-title"}):
                    tutorial = {}
                    tutorial["tutorial_name"] = cur_tutorial.find("strong").getText()
                    tutorial["tutorial_persons"] = cur_tutorial.find("strong").next_sibling.strip()
                    tutorials.append(tutorial)
                session["session_tutorials"] = tutorials
            # session workshop
            elif classes[2] == "session-workshops":
                workshops = []
                for cur_workshop in child.findChildren("span", {"class": "workshop-title"}):
                    workshop = {}
                    workshop["workshop_name"] = cur_workshop.find("strong").getText()
                    try:
                        workshop["workshop_time"] = cur_workshop.find("strong").next_sibling.strip()
                    except:
                        workshop["workshop_time"] = None
                    workshops.append(workshop)
                session["session_workshops"] = workshops

            sessions.append(session)

        elif classes[1] in ["session-break", "session-plenary"]:
            session = {}
            session["session_title"] = child.find("span", {"class": "session-title"}).getText()
            session["session_time"] = child.find("span", {"class": "session-time"}).getText()
            sessions.append(session)

    # session box of a main conference day
    elif classes[0] == "session-box":
        session = {}
        session["session_title"] = child.find("div", {"class": "session-header"}).getText()
        session_boxes = []
        for box in child.findChildren("div", {"class": "session"}):
            box_type = "paper"

            # session poster
            if box.get("class")[2] == "session-posters":
                box_type = "poster"
            session_subbox = {}
            session_subbox["session_title"] = box.find("a", {"class": "session-title"}).get_text()
            session_subbox["session_time"] = box.find("span", {"class": "session-time"}).get_text()
            papers = []
            for paper_detail in box.findChildren("tr", {"id": box_type}):
                paper = {}
                paper["paper_title"] = paper_detail.find("span", {"class": box_type+"-title"}).get_text()
                if box_type == "paper":
                    paper["paper_time"] = paper_detail.find("td", {"id": box_type+"-time"}).get_text()
                paper["paper_author"] = paper_detail.find("em").get_text()
                paper["paper_link"] = paper_detail.find("i")['data']
                papers.append(paper)
            session_subbox["session_"+box_type] = papers
            session_boxes.append(session_subbox)
        session["session_sections"] = session_boxes
        sessions.append(session)
conference[current_day] = sessions

with open('emnlp2019Schedule.json', 'w', encoding='utf-8') as json_file:
    json.dump(conference, json_file, ensure_ascii=False)

#print(json.dumps(conference, indent=1))




