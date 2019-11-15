"""EMNLP 2019 conference crawler"""
__author__= "Lars Meister"

import json

from EMNLP_2019.crawler import tutorial_crawler, workshop_crawler, keynote_crawler


def collect_data():
    conf_dict = generate_conference_dummy_dict()
    #print(json.dumps(conf_dict, indent=1))
    conf_dict["tutorials"] = tutorial_crawler.extract_tutorials()
    conf_dict["workshops"] = workshop_crawler.extract_workshops()
    conf_dict["keynotes"] = keynote_crawler.extract_keynotes()
    # TODO need papers and general information

    with open("output/emnlp2019_data.json", "w") as f:
        json.dump({"EMNLP2019": conf_dict}, f)
    print("created conference data!")


def generate_conference_dummy_dict():
    with open("conference_template.json", "r") as template:
        return json.load(template)

if __name__ == "__main__":
    collect_data()