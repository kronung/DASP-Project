__author__ = "Aron Kaufmann"

import json
from confcrawler.coling2020 import coling_tutorials, COLING_2020_workshop_crawler, coling2020_organizers


def collect_data():
    conf_dict = generate_conference_dummy_dict()
    # print(json.dumps(conf_dict, indent=1))
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
    conf_dict["tutorials"] = coling_tutorials.get_tutorials()
    conf_dict["workshops"] = COLING_2020_workshop_crawler.get_workshops()
    #conf_dict["keynotes"] = keynote_crawler.extract_keynotes()
    #conf_dict["papers"] = paper_crawler.get_papers()

    with open("output/coling2020_data.json", "w", encoding='utf-8') as f:
        json.dump({"COLING2020": conf_dict}, f, ensure_ascii=False)
    print("created conference data!")


def generate_conference_dummy_dict():
    with open("conference_template.json", "r") as template:
        return json.load(template)["conference"]


if __name__ == "__main__":
    collect_data()
