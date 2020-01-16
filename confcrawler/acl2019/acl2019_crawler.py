__author__ = "Aron Kaufmann"

import json
from confcrawler.acl2019.crawler import paper_crawler, tutorials_crawler, workshop_crawler


def collect_data():
    conf_dict = generate_conference_dummy_dict()
    # print(json.dumps(conf_dict, indent=1))
    #conf_dict["topics"] = topics_crawler.extract_topics()
    #conf_dict["organizers"] = organizers_crawler.extract_organizers()
    #conf_dict["submission_deadlines"] = submission_deadlines_crawler.extract_submission_deadlines()
    conf_dict["name"] = "ACL 2019"
    conf_dict["location"] = "Florence, Italy"
    conf_dict["datetime"] = "Juli 28 to August 2, 2019"
    conf_dict["tutorials"] = tutorials_crawler.get_tutorials()
    conf_dict["workshops"] = workshop_crawler.get_workshops()
    #conf_dict["keynotes"] = keynote_crawler.extract_keynotes()
    conf_dict["papers"] = paper_crawler.get_papers()

    with open("output/acl2019_data.json", "w", encoding='utf-8') as f:
        json.dump({"ACL2019": conf_dict}, f, ensure_ascii=False)
    print("created conference data!")


def generate_conference_dummy_dict():
    with open("crawler/conference_template.json", "r") as template:
        return json.load(template)["conference"]


if __name__ == "__main__":
    collect_data()
