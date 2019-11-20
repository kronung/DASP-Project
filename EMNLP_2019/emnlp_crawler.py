"""EMNLP 2019 conference crawler"""
__author__= "Lars Meister"

import json

from EMNLP_2019.crawler import tutorial_crawler, workshop_crawler, keynote_crawler, paper_crawler, \
    topics_crawler, organizers_crawler, submission_deadlines_crawler


def collect_data():
    conf_dict = generate_conference_dummy_dict()
    #print(json.dumps(conf_dict, indent=1))
    conf_dict["topics"] = topics_crawler.extract_topics()
    conf_dict["organizers"] = organizers_crawler.extract_organizers()
    conf_dict["submission_deadlines"] = submission_deadlines_crawler.extract_submission_deadlines()
    conf_dict["name"] = "EMNLP 2019"
    conf_dict["tutorials"] = tutorial_crawler.extract_tutorials()
    conf_dict["workshops"] = workshop_crawler.extract_workshops()
    conf_dict["keynotes"] = keynote_crawler.extract_keynotes()
    conf_dict["papers"] = paper_crawler.extract_papers()

    with open("output/emnlp2019_data.json", "w", encoding='utf-8') as f:
        json.dump({"EMNLP2019": conf_dict}, f, ensure_ascii=False)
    print("created conference data!")


def generate_conference_dummy_dict():
    with open("conference_template.json", "r") as template:
        return json.load(template)["conference"]

if __name__ == "__main__":
    collect_data()