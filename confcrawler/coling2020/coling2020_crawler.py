__author__ = "Aron Kaufmann"

import json
from confcrawler.coling2020 import coling_tutorials, COLING_2020_workshop_crawler, coling2020_organizers
import confcrawler.util.util as util

def collect_data():
    conf_dict = util.generate_empty_conf_dict()
    #conf_dict["topics"] = topics_crawler.extract_topics()
    conf_dict["organizers"] = coling2020_organizers.get_organizers()
    conf_dict["submission_deadlines"] = [
       {
         "name": "Final submissions due",
         "datetime": "8 April (Wednesday) 2020"
       },
       {
         "name": "Notifications",
         "datetime": "10 June 2020 (Wednesday)"
       },
       {
         "name": "Camera-ready (PDF) due",
         "datetime": "30 June 2020 (Tuesday)"
       },
       {
         "name": "Tutorials & Workshops Pre-Conference",
         "datetime": "13-14 September 2020 (Sunday - Monday)"
       },
       {
         "name": "Main Conference",
         "datetime": "15-18 September 2020 (Tuesday - Friday)"
       }
     ]
    conf_dict["name"] = "COLING 2020"
    conf_dict["location"] = "Barcelona, Spain"
    conf_dict["datetime"] = "September 13 to 18, 2020"
    conf_dict["tutorials"] = coling_tutorials.get_tutorials()
    conf_dict["workshops"] = COLING_2020_workshop_crawler.get_workshops()
    #conf_dict["keynotes"] = keynote_crawler.extract_keynotes()
    #conf_dict["papers"] = paper_crawler.get_papers()

    util.save_conference_data("COLING2020", conf_dict)
    print("created conference data!")


if __name__ == "__main__":
    collect_data()
