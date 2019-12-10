"""EMNLP 2019 conference crawler"""
__author__= "Lars Meister"

import json

from Generic_Crawler.crawler import tutorial_crawler, workshop_crawler, keynote_crawler, paper_crawler, \
    topics_crawler, organizers_crawler, submission_deadlines_crawler

# URLS dict

conf_naacl19 = {
    'conf_name' : "NAACL 2019",
    'topics_url' : "",
    'organizers_url' : "",
    'schedule_url': "https://naacl2019.org/schedule/",
    'papers_url': "https://naacl2019.org/program/accepted/",
    'workshops_url': "https://naacl2019.org/program/workshops/",
    'tutorials_url': "https://naacl2019.org/program/tutorials/",
    'smd_url': "https://naacl2019.org/"
    }

conf_emnlp19 = {
    'conf_name' : "EMNLP 2019",
    'topics_url' : "https://www.emnlp-ijcnlp2019.org/calls/papers",
    'organizers_url' : "https://www.emnlp-ijcnlp2019.org/calls/papers",
    'schedule_url': "https://www.emnlp-ijcnlp2019.org/program/ischedule/",
    'papers_url': "https://www.emnlp-ijcnlp2019.org/program/accepted/",
    'workshops_url': "https://www.emnlp-ijcnlp2019.org/program/workshops/",
    'tutorials_url': "https://www.emnlp-ijcnlp2019.org/program/tutorials/",
    'smd_url': "https://www.emnlp-ijcnlp2019.org/calls/papers"
    }


def collect_data(conf_dict):
    conf_dict = generate_conference_dummy_dict()
    conf_dict["topics"] = topics_crawler.extract_topics(conf_dict["topics_url"])
    conf_dict["organizers"] = organizers_crawler.extract_organizers(conf_dict["organizers_url"])
    conf_dict["submission_deadlines"] = submission_deadlines_crawler\
        .extract_submission_deadlines(conf_dict["smd_url"])
    conf_dict["name"] = conf_dict["conf_name"]
    conf_dict["tutorials"] = tutorial_crawler.extract_tutorials(conf_dict["tutorials_url"], conf_dict["schedule_url"])
    conf_dict["workshops"] = workshop_crawler.extract_workshops(conf_dict["workshops_url"], conf_dict["schedule_url"])
    conf_dict["keynotes"] = keynote_crawler.extract_keynotes(conf_dict["schedule_url"])
    conf_dict["papers"] = paper_crawler.extract_papers(conf_dict["papers_url"], conf_dict["schedule_url"])

    with open("output/" + conf_dict["conf_name"].replace(" ", "").lower() + "data.json", "w", \
              encoding='utf-8') \
            as f:
        json.dump(conf_dict, f, ensure_ascii=False)
    print("created conference data!")


def generate_conference_dummy_dict():
    with open("conference_template.json", "r") as template:
        return json.load(template)

if __name__ == "__main__":
    collect_data(conf_naacl19)
    collect_data(conf_emnlp19)
