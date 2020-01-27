"""Conference crawler routine"""
__author__= "Lars Meister"

import json
import logging
import time
from confcrawler.util import util

from confcrawler.universalcrawler.crawler import organizers_crawler, keynote_crawler, paper_crawler, \
    workshop_crawler, topics_crawler, submission_deadlines_crawler, tutorial_crawler

# URLS dict just for testing

conf_naacl19 = {
    'conf_name' : "NAACL 2019",
    'topics_url' : "",
    'organizers_url' : "",
    'schedule_url': "https://naacl2019.org/schedule/",
    'papers_url': "https://naacl2019.org/program/accepted/",
    'workshops_url': "https://naacl2019.org/program/workshops/",
    'tutorials_url': "https://naacl2019.org/program/tutorials/",
    'keynotes_url' : "https://naacl2019.org/program/keynotes/",
    'smd_url': "https://naacl2019.org/"
    }

conf_emnlp19 = {
    'conf_name' : "EMNLP 2019",
    'topics_url' : "https://www.emnlp-ijcnlp2019.org/calls/papers",
    'organizers_url' : "https://www.emnlp-ijcnlp2019.org/organization",
    'schedule_url': "https://www.emnlp-ijcnlp2019.org/program/ischedule/",
    'papers_url': "https://www.emnlp-ijcnlp2019.org/program/accepted/",
    'workshops_url': "https://www.emnlp-ijcnlp2019.org/program/workshops/",
    'tutorials_url': "https://www.emnlp-ijcnlp2019.org/program/tutorials/",
    'keynotes_url' : "https://www.emnlp-ijcnlp2019.org/program/keynotes/",
    'smd_url': "https://www.emnlp-ijcnlp2019.org/calls/papers"
    }

conf_acl20 = {
    'conf_name' : "ACL 2020",
    'topics_url' : "https://acl2020.org/calls/demos/",
    'organizers_url' : "",
    'schedule_url': "",
    'papers_url': "",
    'workshops_url': "https://acl2020.org/program/workshops/",
    'tutorials_url': "https://acl2020.org/program/tutorials/",
    'keynotes_url' : "",
    'smd_url': "https://acl2020.org/"
    }


def collect_data(conf_file, folder):
    """Collects the crawled data for a conf_file and saves it to a file."""

    conf_dict = util.generate_empty_conf_dict()
    conf_dict["name"] = conf_file["conf_name"]

    try:
        conf_dict["topics"] = topics_crawler.extract_topics(conf_file["topics_url"])
    except Exception:
        logging.exception("Fatal error in topics_crawler!")

    try:
        conf_dict["organizers"] = organizers_crawler.extract_organizers(conf_file["organizers_url"])
    except Exception:
        logging.exception("Fatal error in organizer_crawler!")

    try:
        conf_dict["submission_deadlines"] = submission_deadlines_crawler\
            .extract_submission_deadlines(conf_file["smd_url"])
    except Exception:
        logging.exception("Fatal error in smd_crawler!")

    try:
        conf_dict["tutorials"] = tutorial_crawler.extract_tutorials(conf_file["tutorials_url"],
                                                                conf_file["schedule_url"])
    except Exception:
        logging.exception("Fatal error in tutorial_crawler!")

    try:
        conf_dict["workshops"] = workshop_crawler.extract_workshops(conf_file["workshops_url"],
                                                                conf_file["schedule_url"])
    except Exception:
        logging.exception("Fatal error in workshop_crawler!")

    try:
        conf_dict["keynotes"] = keynote_crawler.extract_keynotes(conf_file["keynotes_url"],
                                                                 conf_file["schedule_url"])
    except Exception:
        logging.exception("Fatal error in keynote_crawler!")
    try:
        conf_dict["papers"] = paper_crawler.extract_papers(conf_file["papers_url"],
                                                           conf_file["schedule_url"])
    except Exception:
        logging.exception("Fatal error in papers_crawler!")

    util.save_conference_data(conf_file["conf_name"], conf_dict, folder)


def start_crawling(conf_file, folder):
    """Routine to crawl data."""
    # initialise logger
    logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s:%(message)s',
                        level=logging.DEBUG,
                        datefmt='%H:%M:%S',
                        handlers=[logging.FileHandler('confcrawler/logs/confcrawler.log', 'w',
                                                      'utf-8')])
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

    logging.info('Start conference crawling...')
    logging.info('---------- Conference to crawl: %s', conf_file["conf_name"])
    start = time.time()
    collect_data(conf_file, folder)
    end = time.time()
    logging.info('--- %s DONE, data crawled in %s seconds', conf_file["conf_name"],
                 round(end-start, 3))

    logging.info('Completed crawling')
