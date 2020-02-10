#!/usr/bin/env python3
"""Script to create sql dump file from json data files."""

__author__ = "Lars Meister, Samaun Ibna Faiz, Aron Kaufmann, Yuqing Xu"

import os
from sys import argv
import traceback
import json

def run():
    if len(argv) == 1 or argv[1] in ["help", "-help"]:
        help()
        return

    if len(argv) in [2, 3]:
        output_folder = 'sql'
        if len(argv) == 3:
            output_folder = argv[2]
        try:
            if os.path.exists(argv[1]):
                output = open(output_folder + "/data.sql", "w", encoding='utf-8')
                output.write(create_db_scheme())
                for file in os.listdir(argv[1]):
                    path = argv[1] + "/" + file
                    output.write(read_file(path))
                output.close()
                print("DONE: data.sql file created! at {} folder!".format(output_folder))
            else:
                print("Given directory does not exist!")

        except Exception:
            traceback.print_exc()
            print("Could not read data files!")
def help():
    print("--- confcrawler sql generator version 1.0 UKP Lab TU Darmstadt python3 ---\n\n"
          "Confcrawler sql generator help instructions:\n\n"
          "Lets you generate a sql dump file to create a sql database \n"
          "from the conference json data files."
          " How to use this program:\n"
          "Open terminal, navigate to the root folder of the programm 'DASP-Project'\n"
          "Type via Terminal:\n"
          "python3 create_database_dump.py YOUR_FILEPATH_TO_THE_DATA_FOLDER "
          "OUTPUT_FOLDER_FILEPATH\n\n"
          "Parameter:\n"
          "-THE_DATA_FOLDER - filepath to folder where the conference data files are stored:\n\n"
          "The folder must only contain .json data files of crwaled conferences. See conf crawler\n"
          " README for details on the json files. Default folder DASP-Project -> data\n"
          "needs to be specified in any case.\n\n"
          "- OUTPUT_FOLFER_FILEPATH (optional, default output is saved to sql folder of "
          "program).\n\n\n"
          "Example calls:\n\n"
          "python3 create_database_dump.py data\n"
          "python3 create_database_dump.py data /user/folder1/folder2"
          )


def read_file(file):
    """Reads in a data file and """
    rs = "\n"
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)
        rs += "INSERT INTO Conference (conf_name) VALUES ('{}');\n".format(data["name"])

        # Insert paper
        for paper in data["papers"]:
            ps = ""
            ps += """INSERT INTO Paper (PK_conf, paper_title, paper_keywords, paper_link, paper_type, paper_time)
             VALUES ("{}", "{}", "{}", "{}", "{}", "{}");\n""" \
                .format(data["name"], paper["paper_title"],
                        paper["paper_keywords"], paper["paper_link"], paper["paper_type"],
                        paper["paper_time"])
            for author in paper["paper_authors"]:
                try:
                    given_name, family_name = author.rsplit(' ', 1)
                except ValueError:
                    family_name = author
                    given_name = None

                ps += """INSERT IGNORE INTO Author (family_name, given_name) VALUES ("{}", "{}");\n"""\
                    .format(family_name, given_name)

                ps += """INSERT INTO Paper_Author_Rel (PK_author_fn, PK_author_gn, PK_paper) 
                VALUES ("{}", "{}", "{}");\n""" \
                    .format(family_name, given_name, paper["paper_title"])
            rs += ps.replace("\"None\"", "NULL")

        # Insert tutorials
        for tutorial in data["tutorials"]:
            try:
                tutorial_author = ", ".join(tutorial["tutorial_author"])
            except TypeError:
                tutorial_author = None
            ts = ""
            ts += """INSERT INTO Tutorial (PK_conf, tutorial_author, tutorial_name, tutorial_abstract, tutorial_location, tutorial_time, tutorial_link)
             VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}");\n""" \
                .format(data["name"], tutorial_author,
                        tutorial["tutorial_name"], tutorial["tutorial_abstract"], tutorial["tutorial_location"],
                        tutorial["tutorial_time"], tutorial["tutorial_link"])

            rs += ts.replace("\"None\"", "NULL")

        # Insert workshops
        for workshop in data["workshops"]:
            try:
                workshop_organizer = ", ".join(workshop["workshop_organizer"])
            except TypeError:
                workshop_organizer = None

            ws = ""
            ws += """INSERT INTO Workshop (PK_conf, workshop_name, workshop_organizer, workshop_description, workshop_day, workshop_location, workshop_link) 
            VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}");\n""" \
                .format(data["name"], workshop["workshop_name"],
                        workshop_organizer, workshop["workshop_description"],
                        workshop["workshop_day"], workshop["workshop_location"],
                                  workshop["workshop_link"])

            rs += ws.replace("\"None\"", "NULL")

        # Insert keynotes
        for keynote in data["keynotes"]:
            ks = ""
            ks += """INSERT INTO Keynote (PK_conf, keynote_title, keynote_speaker, keynote_speaker_bio, keynote_abstract, keynote_time, keynote_location, keynote_link) 
            VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");\n""" \
            .format(data["name"], keynote["keynote_title"],
                    keynote["keynote_speaker"], keynote["keynote_speaker_bio"],
                              keynote["keynote_abstract"], keynote["keynote_time"],
                              keynote["keynote_location"], keynote["keynote_link"])

            rs += ks.replace("\"None\"", "NULL")

    return rs

def create_db_scheme():
    with open("confcrawler/ressources/db_scheme.txt", "r") as f:
        return f.read()


run()