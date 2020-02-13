"""Util functions."""
__author__ = "Lars Meister, Samaun Ibna Faiz, Aron Kaufmann"

import json
from re import sub
import pathlib

current_path = pathlib.Path(__file__).parent.parent.parent


def generate_empty_conf_dict():
    """Generates an empty dictionary according to the conference template."""
    with open(str(current_path) + "/confcrawler/ressources/conference_template.json", "r") as template:
        return json.load(template)


def load_conference(filepath):
    """Loads existing conf data into dictionary."""
    with open(filepath, "r", encoding='utf-8') as f:
        return json.load(f)


def save_conference_data(conf_name, conf_data, folder="/data"):
    """Saves the generated conf_data dict to file in the output folder."""
    with open(str(current_path) + folder + "/" + conf_name.replace(" ", "").lower() + "_data.json", "w",
              encoding='utf-8') as f:
        json.dump(conf_data, f, ensure_ascii=False)


def basic_string_clean(string):
    """Basic string cleaning."""
    filter1 = sub(r'([\n\t]|^\s+|\s+$)', "", string)
    return filter1.replace("\"", "'")


def find_next_sibling_line(element, tag_type):
    """
    Gets current elements next sibling's (chosen by provided tag_type) actual line number in html document

    :param element: Whose sibling to look for, type: An object of class bs4.Tag
    :param tag_type: sibling tag's type (e.g. p, h2, div, span etc. ), type: A string
    :return: An Integer specifying line no. in html, infinite when no sibling is found
    """
    nxt_sib = element.find_next_sibling(tag_type)
    return float("inf") if nxt_sib is None else nxt_sib.sourceline


def find_next_sibling_position(element, tag_type):
    """
    Gets current elements next sibling's (chosen by provided tag_type) actual character position in html document

    :param element: Whose sibling to look for, type: An object of class bs4.Tag
    :param tag_type: sibling tag's type (e.g. p, h2, div, span etc. ), type: A string
    :return: An Integer specifying character pos. in html, infinite when no sibling is found
    """
    nxt_sib = element.find_next_sibling(tag_type)
    return float("inf") if nxt_sib is None else nxt_sib.sourcepos


def pre_process_types(elements):
    """
    Enhances the given list of tags(elements) with sentinel information and returns the result

    :param elements: List of bs4.tag object
    :return: Tag extended with additional information as dictionary in list elements
    """
    return [
        {
            'elem': e,
            'nxt_sib_line': find_next_sibling_line(e, e.name),
            'nxt_sib_pos': find_next_sibling_position(e, e.name)
        }
        for e in elements
    ]


def is_proper_sibling(element, parent):
    """
    Checks if the element(sibling) should be considered as a sibling of parent's['elem'] or not

    :param element: A Tag object to be tested for sibling candidacy
    :param parent: A dictionary object containing a Tag(parent) object and position information of the nex sentinel
    :return: If we should consider the give element as proper sibling or not
    """
    return (
               element.sourcepos - parent['nxt_sib_pos']
               if element.sourceline - parent['nxt_sib_line'] == 0
               else element.sourceline - parent['nxt_sib_line']
           ) < 0


def get_proper_siblings(parent_tag, sibling_tag_name):
    """
    Prunes out improper siblings and gives back the appropriate ones.

    :param parent_tag: A Dictionary containing Tag objects with extended infos. respect to which we look for proper siblings
    :param sibling_tag_name: sibling tag's type (e.g. p, h2, div, span etc. ), type: A string
    :return: A List of proper siblings of sibling_tag_name type
    """
    all_siblings = parent_tag['elem'].find_next_siblings(sibling_tag_name)
    try:
        first_improper_sibling = next(
            i for i, e in enumerate(all_siblings) if not is_proper_sibling(e, parent_tag)
        )
    except StopIteration:
        return all_siblings

    return all_siblings[:first_improper_sibling]

