#!/usr/bin/env python3
"""Main entry point."""

from confcrawler.util import util
from confcrawler.queries import queries
from confcrawler import conference_crawler
import traceback

from sys import argv

# python3 confcrawler.py conf_file (output_location)
# python3 confcrawler.py -help

def help():
    print("--- confcrawler version 1.0 UKP Lab TU Darmstadt python3 ---\n\n"
          "Confcrawler help instructions:\n\n"
          "confcrawler lets you crawl data for specific nlp conference websites,\n"
          "which have the same html template than emnlp2019 or naacl2019.\n"
          "It tries to extract as much information as it can for the provided urls\n"
          "to generate a conference.json file with the structured data.\n\n"
          "How to use this program:\n"
          "Open terminal, navigate to the root folder of the programm 'DASP-Project'\n"
          "Type via Terminal:\n"
          "python3 confcrawler.py YOUR_FILEPATH_TO_CONF_FILE.TXT OUTPUT_FOLDER_FILEPATH\n\n"
          "Parameter:\n"
          "-CONF_FILE.txt - filepath to txt file of the form:\n\n"
          "conf_name = NAACL 2019\n"
          "topics_url = \n"
          "organizers_url = \n"
          "schedule_url = https://naacl2019.org/schedule/\n"
          "papers_url = https://naacl2019.org/program/accepted/\n"
          "workshops_url = https://naacl2019.org/program/workshops/\n"
          "tutorials_url = https://naacl2019.org/program/tutorials/\n"
          "keynotes_url = https://naacl2019.org/program/keynotes/\n"
          "smd_url = https://naacl2019.org/\n\n"
          "only change the urls, not the the property names, if no url leave empty.\n\n"
          "- OUTPUT_FOLFER_FILEPATH (optional, default output is saved to data folder of "
          "program)\n"
          )
def run():
    if len(argv) == 1 or argv[1] in ["help", "-help"]:
        help()
        return

    if len(argv) in [2, 3]:
        folder = ""
        if len(argv) == 3:
            folder = argv[2]
        try:
            conf_urls = {}
            with open(argv[1], "r") as f:
                for line in f.readlines():
                    line_list = [i.strip() for i in line.replace("\n", "").split("=")]
                    conf_urls[line_list[0]] = line_list[1]

            conference_crawler.start_crawling(conf_urls, folder)

        except Exception:
            traceback.print_exc()
            print("Could not read conf_file!")


run()
