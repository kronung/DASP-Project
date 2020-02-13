__author__ = "Aron Kaufmann"

import json
from confcrawler.acl2019.crawler import paper_crawler, tutorials_crawler, workshop_crawler, organizers_crawler
import confcrawler.util.util as util


def collect_data():
    conf_dict = util.generate_empty_conf_dict()
    # print(json.dumps(conf_dict, indent=1))
    #conf_dict["topics"] = topics_crawler.extract_topics()
    conf_dict["organizers"] = organizers_crawler.get_organizers()
    conf_dict["submission_deadlines"] = [
        {
            "name": "Submission deadline (long & short papers)",
            "datetime": "4 March, 2019"
        },
        {
            "name": "Notification of acceptance",
            "datetime": "13 May, 2019"
        },
        {
            "name": "Camera-ready due",
            "datetime": "3 June, 2019"
        },
        {
            "name": "Tutorials",
            "datetime": "28 July, 2019"
        },
        {
            "name": "Conference",
            "datetime": "29 to 31 July, 2019"
        },
        {
            "name": "Workshops and Co-located conferences",
            "datetime": "1 to 2 August, 2019"
        }
    ]
    conf_dict["name"] = "ACL 2019"
    conf_dict["location"] = "Florence, Italy"
    conf_dict["datetime"] = "Juli 28 to August 2, 2019"
    conf_dict["tutorials"] = tutorials_crawler.get_tutorials()
    conf_dict["workshops"] = workshop_crawler.get_workshops()
    #conf_dict["keynotes"] = keynote_crawler.extract_keynotes()
    conf_dict["papers"] = paper_crawler.get_papers()

    util.save_conference_data("ACL2019", conf_dict, "data")
    print("created conference data!")


if __name__ == "__main__":
    collect_data()
