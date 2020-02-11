__author__ = "Samaun Ibna Faiz"

import json
from typing import List, Dict, Any

from bs4 import Tag
from fuzzywuzzy import process


def find_next_sibling_line(element: Tag, tag_type: str) -> int:
    """
    Gets current elements next sibling's (chosen by provided tag_type) actual line number in html document

    :param element: Whose sibling to look for, type: An object of class bs4.Tag
    :param tag_type: sibling tag's type (e.g. p, h2, div, span etc. ), type: A string
    :return: An Integer specifying line no. in html, infinite when no sibling is found
    """
    nxt_sib = element.find_next_sibling(tag_type)
    return float("inf") if nxt_sib is None else nxt_sib.sourceline


def find_next_sibling_position(element: Tag, tag_type: str) -> int:
    """
    Gets current elements next sibling's (chosen by provided tag_type) actual character position in html document

    :param element: Whose sibling to look for, type: An object of class bs4.Tag
    :param tag_type: sibling tag's type (e.g. p, h2, div, span etc. ), type: A string
    :return: An Integer specifying character pos. in html, infinite when no sibling is found
    """
    nxt_sib = element.find_next_sibling(tag_type)
    return float("inf") if nxt_sib is None else nxt_sib.sourcepos


def pre_process_types(elements: List[Tag]) -> List[Dict[str, Any]]:
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


def is_proper_sibling(element: Tag, parent: Dict[str, Any]) -> bool:
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


def get_proper_siblings(parent_tag: Dict[str, Any], sibling_tag_name: str) -> List[Tag]:
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


def validate_unique_hash(item_list: List[Dict[str, Any]], list_name: str = None) -> None:
    """
    Checks for uniqueness of the generated hash. Please note that it is not guaranteed that generated hash values will
    be unique for different contents. md5 guaranties only a change in content will result in different hash.


    :param item_list: A List of dictionaries, must contain the key `hash` also the list must be sorted using this key for faster and correct processing.
    :param list_name: A human friendly name of the list, to be used by logger.
    :return: No return value.
    """
    print('Comparing hash for {}'.format(list_name))  # can be changed into logging

    # since the list is expected to be sorted on key `hash` any duplicate must be in single index distance apart
    for i in range(len(item_list) - 1):
        if item_list[i]['hash'] == item_list[i + 1]['hash']:
            print('conflict found...')
            print(item_list[i])
            print(item_list[i + 1])


def print_debug(msg: str, debug: bool) -> None:
    """
    A helper function for printing debug message to console

    :param msg: The message as a string
    :param debug: A boolean; will result in output only when True
    :return: No return value.
    """
    if debug:
        print(msg)  # can be replaced by logger function


# todo: Make this method generic on multiple properties
def check_for_duplicates(item_list1: List[Dict[str, Any]], item_list2: List[Dict[str, Any]],
                         l1_name: str, l2_name: str, debug: bool = False) -> bool:
    """
    A function that that checks there is no duplicate between List of papers
    (For example: `poster paper`s and `session paper`s) obtained from 2 different sources;
    uses plain string matching on `Hash` and `Authors` property.

    :param item_list1: A List of dictionaries, Must contain `Hash` and `Authors` property.
    :param item_list2: A List of dictionaries, Must contain `Hash` and `Authors` property.
    :param l1_name: A human friendly name of the first list, to be used by logger.
    :param l2_name: A human friendly name of the second list, to be used by logger.
    :param debug: A boolean; will print console messages only when True
    :return: A boolean; Reports True if none of the papers have a duplicate; False otherwise.
    """

    print("Checking for common elements between list {} and {}".format(l1_name, l2_name))  # log

    no_duplicate = True
    paper_hashes_l1 = [p['hash'] for p in item_list1]
    paper_authors_l1 = [",".join(p['authors']) for p in item_list1]

    for p in item_list2:
        authors = ",".join(p['authors'])
        has_common_title = any(p['hash'] == h for h in paper_hashes_l1)
        has_common_author = any(authors == a for a in paper_authors_l1)
        if has_common_title:
            print_debug(
                "Found duplicate in title. Title: {}, Sub-Session: {}".format(p['title'], p['sub_session']),
                debug
            )
            no_duplicate = False
        elif has_common_author:
            print_debug(
                "Found duplicate in authors. Title: {}, Authors: {}, Sub-Session: {}".format(p['title'], authors,
                                                                                             p['sub_session']),
                debug
            )
            no_duplicate = False

    if no_duplicate:
        print("No Duplicate found")
    else:
        print("Duplicate(s) found")

    return not no_duplicate


# todo: Make this method generic on multiple properties
# Also custom ratio(score_cutoff) instead of 100% can be supplied as parameters to be used with different properties
def fuzzy_check_for_duplicates(item_list1: List[Dict[str, Any]], item_list2: List[Dict[str, Any]],
                               l1_name: str, l2_name: str, debug: bool = False) -> bool:
    """
    A function that that checks there is no duplicate between List of papers
    (For example: `poster paper`s and `session paper`s) obtained from 2 different sources;
    uses fuzzy string matching on `title` and `Authors` property.

    :param item_list1: A List of dictionaries, Must contain `title`, `Authors` and `sub_session` property.
    :param item_list2: A List of dictionaries, Must contain `title`, `Authors` and `sub_session` property.
    :param l1_name: A human friendly name of the first list, to be used by logger.
    :param l2_name: A human friendly name of the second list, to be used by logger.
    :param debug: A boolean; will print console messages only when True
    :return: A boolean; Reports True if none of the papers have a duplicate; False otherwise.
    """
    print("Checking for common elements using fuzzy match between list {} and {}".format(l1_name, l2_name))

    no_duplicate = True
    paper_titles_l1 = [p['title'] for p in item_list1]
    paper_authors_l1 = [", ".join(p['authors']) for p in item_list1]

    for p in item_list2:
        authors = ", ".join(p['authors'])

        (title, t_ratio) = process.extractOne(p['title'], paper_titles_l1)
        (author, a_ratio) = process.extractOne(", ".join(p['authors']), paper_authors_l1)

        if t_ratio < 100.0 and a_ratio < 100.0:
            continue

        if a_ratio < t_ratio:
            print_debug(
                "Found duplicate in title. Title: {}: Sub-Session: {}".format(p['title'], p['sub_session']),
                debug
            )
            no_duplicate = False
        else:
            print_debug(
                "Found duplicate in authors. Title: {}, Authors: {}, Sub-Session: {}".format(p['title'], authors,
                                                                                             p['sub_session']),
                debug
            )
            no_duplicate = False

    if no_duplicate:
        print("No Duplicate found")
    else:
        print("Duplicate(s) found")

    return not no_duplicate


# todo: Make this method generic on multiple properties
def merge_list(item_list1: List[Dict[str, Any]], item_list2: List[Dict[str, Any]], debug: bool = False) \
        -> (List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]):
    """
    Given two lists of papers it merges them based on `hash` values equality. Both of the lists must have Non-empty
    values for `hash`, `title` and `authors` properties, Also must be ascending sorted on `hash` key. Uses plain string
    matching. Only copies `type` property from first list to second.

    :param item_list1: A List of dictionaries, Must contain Non-empty values for `hash`, `title` and `authors` property.
    :param item_list2: A List of dictionaries, Must contain Non-empty values for `hash`, `title` and `authors` property.
    :param debug: A boolean; will print console messages only when True
    :return: A tuple containing 3 list of dictionaries first the successful merge result of two lists, then the unmerged items from first list followed by the unmerged item from the second list.
    """
    (l1, l2, is_swapped) = \
        (item_list2, item_list1, True) if len(item_list1) < len(item_list2) else (item_list1, item_list2, False)

    unmatched_paper_list1, unmatched_paper_list2, merged_paper_list = [], [], []
    print("String Matching and merging two lists .....")

    j = 0
    for i in range(len(l1)):
        if j == len(l2):
            break

        if l2[j]['hash'] != l1[i]['hash']:
            unmatched_paper_list1.append(l1[i])

        if l2[j]['hash'] < l1[i]['hash']:
            if debug:
                print('Matched failed with j: {}'.format(j))
            fp = l2[j]
            if debug:
                print(fp)
            unmatched_paper_list2.append(fp)
            j += 1

        elif l1[i]['hash'] == l2[j]['hash']:

            if l1[i]['title'] != l2[j]['title']:
                if debug:
                    print('conflict found... hash matched but title did not')
                    print(l1[i])
                    print(l2[j])

            elif ",".join(l1[i]['authors']) != ",".join(l2[j]['authors']):
                if debug:
                    print('conflict found... hash matched but authors did not')
                    print(l1[i])
                    print(l2[j])
                p = {**l1[j], **{'type': l2[i]['type']}} if is_swapped else {**l2[j], **{'type': l1[i]['type']}}
                merged_paper_list.append(p)

            else:
                # print('Matched i : {} with j: {}'.format(i, j))
                p = {**l1[j], **{'type': l2[i]['type']}} if is_swapped else {**l2[j], **{'type': l1[i]['type']}}
                merged_paper_list.append(p)
                # print(l1[i])
                # print(l2[j])
            j += 1

    # no_match_paper_list.sort(key=lambda x: x['hash'])
    if is_swapped:
        (unmatched_paper_list1, unmatched_paper_list2, i, j) = (unmatched_paper_list2, unmatched_paper_list1, j, i)

    print("Among {} form list1, {} from list2, {} matched.\nNot matched {} in list1, {} in list2".format(
        i, j, len(merged_paper_list), len(unmatched_paper_list1), len(unmatched_paper_list2)
    ))

    return merged_paper_list, unmatched_paper_list1, unmatched_paper_list2


# todo: Make this method generic on multiple properties
# def fuzzy_merge_list(item_list1: List[Dict[str, Any]], item_list2: List[Dict[str, Any]], threshold: float,
# Good matches always shows 100%; no need to use threshold
def fuzzy_merge_list(item_list1: List[Dict[str, Any]], item_list2: List[Dict[str, Any]], debug: bool = True) \
        -> (List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]):
    """
    Given two lists of papers it merges them based on `title` and `authors` values. Both of the lists must have
    Non-empty values for `hash`, `title` and `authors` properties. Uses fuzzy string matching. Only copies `type`
    property from first list to second.

    :param item_list1: A List of dictionaries, Must contain Non-empty values for `title` and `authors` property.
    :param item_list2: A List of dictionaries, Must contain Non-empty values for `title` and `authors` property.
    :param debug: A boolean; will print console messages only when True
    :return: A tuple containing 3 list of dictionaries first the successful merge result of two lists, then the unmerged items from first list followed by the unmerged item from the second list.
    """
    def process_dicts(item1: Dict[str, Any], item2: Dict[str, Any], merged_list: List[Dict[str, Any]],
                      source_list: List[Dict[str, Any]], ratio: float) -> None:
        mp = {**item1, **{'type': item2['type']}}
        merged_list.append(mp)
        source_list.append({
            't1': p1['title'], 'a1': ", ".join(p1['authors']), 'h1': p1['hash'],
            't2': item1['title'], 'a2': ", ".join(item1['authors']), 'h2': item1['hash'],
            'ratio': ratio
        })

    merged_paper_list = []
    likely_merged_paper_list_on_title = []
    likely_merged_paper_list_on_author = []
    unmatched_list1_after_merge = []
    unmatched_list2_after_merge = []

    print("Fuzzy Matching and merging two lists .....")

    paper_titles_l1 = [p['title'] for p in item_list1]
    paper_authors_l1 = [", ".join(p['authors']) for p in item_list1]

    for p in item_list2:

        (title, t_ratio) = process.extractOne(p['title'], paper_titles_l1)
        (author, a_ratio) = process.extractOne(", ".join(p['authors']), paper_authors_l1)

        if t_ratio < 100.0 and a_ratio < 100.0:
            unmatched_list2_after_merge.append(p)
            continue

        if t_ratio >= a_ratio:
            p1 = next(p for p in item_list1 if p['title'] == title)
            process_dicts(p, p1, merged_paper_list, likely_merged_paper_list_on_title, t_ratio)
        else:
            p1 = next(p for p in item_list1 if ", ".join(p['authors']) == author)
            process_dicts(p, p1, merged_paper_list, likely_merged_paper_list_on_author, a_ratio)

    # for p1 in item_list1:
    #     for p2 in item_list2:
    #         if fuzz.token_set_ratio(p1['title'], p2['title']) >= threshold:
    #             p = {**p2, **{'type': p1['type']}}
    #             merged_paper_list.append(p)
    #             likely_merged_paper_list_on_title.append({
    #                 't1': p1['title'], 'a1': ", ".join(p1['authors']), 'h1': p1['hash'],
    #                 't2': p2['title'], 'a2': ", ".join(p2['authors']), 'h2': p2['hash'],
    #             })
    #         elif fuzz.token_set_ratio(", ".join(p1['authors']), ", ".join(p2['authors'])) >= threshold:
    #             p = {**p2, **{'type': p1['type']}}
    #             merged_paper_list.append(p)
    #             likely_merged_paper_list_on_author.append({
    #                 't1': p1['title'], 'a1': ", ".join(p1['authors']), 'h1': p1['hash'],
    #                 't2': p2['title'], 'a2': ", ".join(p2['authors']), 'h2': p2['hash'],
    #             })

    for p1 in item_list1:
        from_list_one = any(p1['hash'] == p['h1'] for p in likely_merged_paper_list_on_title)
        from_list_two = any(p1['hash'] == p['h1'] for p in likely_merged_paper_list_on_author)
        if not (from_list_one and from_list_two):
            unmatched_list1_after_merge.append(p1)

    # we know which papers were matched form list2
    # for p2 in item_list2:
    #     from_list_one = any(p2['hash'] == p['h2'] for p in likely_merged_paper_list_on_title)
    #     from_list_two = any(p2['hash'] == p['h2'] for p in likely_merged_paper_list_on_author)
    #     if not (from_list_one and from_list_two):
    #         unmatched_list2_after_merge.append(p2)

    if debug:
        likely_merged_paper_list_on_title.sort(key=lambda x: x['ratio'])
        with open('likely_merged_paper_list_on_title.json', 'w') as outfile:
            json.dump(likely_merged_paper_list_on_title, outfile, indent=2)
        likely_merged_paper_list_on_author.sort(key=lambda x: x['ratio'])
        with open('likely_merged_paper_list_on_author.json', 'w') as outfile:
            json.dump(likely_merged_paper_list_on_author, outfile, indent=2)

    print("Fuzzy merged on title: {}, on authors: {}, total after fuzzy merge {}".format(
        len(likely_merged_paper_list_on_title), len(likely_merged_paper_list_on_author), len(merged_paper_list)
    ))

    return merged_paper_list, unmatched_list1_after_merge, unmatched_list2_after_merge


def find_all_indices(txt: str, sub_str: str) -> List[int]:
    offset = len(sub_str)
    return [i for (i, c) in enumerate(txt) if txt[i:i + offset] == sub_str]
