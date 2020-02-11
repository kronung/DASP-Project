__author__ = "Samaun Ibna Faiz"

import hashlib
import json
from urllib import request

from bs4 import BeautifulSoup, SoupStrainer

from util.util import validate_unique_hash, merge_list, fuzzy_merge_list, check_for_duplicates, \
    fuzzy_check_for_duplicates

################################################
# Accepted Paper list                          #
################################################

source = 'https://www.emnlp-ijcnlp2019.org/program/accepted/'

# print(html_doc)
page_content = SoupStrainer('section', class_='page__content')
soup = BeautifulSoup(request.urlopen(source), 'html.parser', parse_only=page_content)

fn_paper_list = [
    {
        'id': "id",
        # Add '.' for making it consistent with session and poster papers
        'title': (t := p.select('span')[0].text.strip() + '.'),
        # We hash for faster(one pass) and consistent plain string merging
        # Also fixed length of hash makes string comparison faster compared to variable and lengthy paper name
        'hash': hashlib.md5(t.encode('utf-8')).hexdigest(),
        'authors': [
            a_
            for a in p.i.get_text().replace(' and ', ',').split(',')
            if len(a_ := a.strip()) > 0
        ],
        # reduce(lambda x, y: x + y, [el.capitalize() for el in e.get_text().split(' ')], ''),
        'type': e.text
    }
    for e in soup.find_all('h2')
    for p in e.find_next_sibling('ul').find_all('li')
]

# print(fn_paper_list)

################################################
# Presented paper list in conference sessions  #
################################################

source = 'https://www.emnlp-ijcnlp2019.org/program/ischedule/'

# print(html_doc)
page_content = SoupStrainer('section', class_='page__content')
soup = BeautifulSoup(request.urlopen(source), 'html.parser', parse_only=page_content)

fn_session_paper_list = [
    {
        'id': p['paper-id'],
        'title': (pt := p.select('span.paper-title')[0].text.strip()),
        # We hash for faster(one pass) and consistent plain string merging
        # Also fixed length of hash makes string comparison faster compared to variable and lengthy paper name
        'hash': hashlib.md5(pt.encode('utf-8')).hexdigest(),
        'authors': [
            a.strip()
            for a in p.select('em')[0].text.replace(' and ', ',').split(',')  # fixme : use 'and' in split in re
            if len(a.strip()) > 0
        ],
        'session': sg.select('div.session-header')[0].text.strip(),  # fixme : Remove enclosing '()' brackets from text
        'sub_session': s.select('a.session-title')[0].text.strip(),  # todo : should it be renamed to Track?
        'weekday': (d := s.select('span.session-time')[0]['title'].split(','))[0].strip(),
        'date': d[1].strip(),
        'start_time': (t := p.select('td#paper-time')[0].text.split('\u2013'))[0].strip(),
        'end_time': t[1].strip(),
        'url': p.select('i.fa-file-pdf-o')[0]['data'],
        'location': s.select('span.session-location')[0].text.strip().replace('\u2013', '-'),
    }
    for sg in soup.select('div.session-box')
    for s in sg.select('div.session')
    for p in s.select('table.paper-table tr#paper')
]

print(fn_session_paper_list)

print(len(fn_paper_list), len(fn_session_paper_list))
# print(fn_paper_list[0]['title'])

# Sorting helps us detect any duplicate in generated hash, also plain string match merge becomes single pass
sorted_paper_list = sorted(fn_paper_list, key=lambda x: x['hash'])
sorted_session_paper_list = sorted(fn_session_paper_list, key=lambda x: x['hash'])

validate_unique_hash(sorted_paper_list, 'paper list from Accepted papers.')

validate_unique_hash(sorted_session_paper_list, 'session paper list from interactive schedule.')

with open('sorted_paper_list_accepted_papers.json', 'w') as outfile:
    json.dump(sorted_paper_list, outfile, indent=2)

with open('sorted_paper_list_iSchedule_sessions.json', 'w') as outfile:
    json.dump(sorted_session_paper_list, outfile, indent=2)

print("Matching papers of two lists .....")

# Plain string match and merge; We will apply fuzzy merging later to only those papers that did not match
merged_paper_list, unmatched_paper_list, unmatched_session_paper_list = merge_list(sorted_paper_list,
                                                                                   sorted_session_paper_list)

with open('no_match_paper_list.json', 'w') as outfile:
    json.dump(unmatched_paper_list, outfile, indent=2)

with open('no_match_session_paper_list.json', 'w') as outfile:
    json.dump(unmatched_session_paper_list, outfile, indent=2)

with open('merged_paper_list.json', 'w') as outfile:
    json.dump(merged_paper_list, outfile, indent=2)

# Applying fuzzy merging to unmatched papers.
fuzzy_merged_paper_list, unmatched_paper_list_after_fuzzy_merge, unmatched_session_paper_list_after_fuzzy_merge \
    = fuzzy_merge_list(unmatched_paper_list, unmatched_session_paper_list, True)
# = fuzzy_merge_list(unmatched_paper_list, unmatched_session_paper_list, 80.0, True)

with open('no_match_paper_list_after_fuzzy_merge.json', 'w') as outfile:
    json.dump(unmatched_paper_list_after_fuzzy_merge, outfile, indent=2)

with open('no_match_session_paper_list_after_fuzzy_merge.json', 'w') as outfile:
    json.dump(unmatched_session_paper_list_after_fuzzy_merge, outfile, indent=2)

with open('fuzzy_merged_paper_list.json', 'w') as outfile:
    json.dump(fuzzy_merged_paper_list, outfile, indent=2)

################################################
# Presented paper list as conference posters   #
################################################

fn_poster_list = [
    {
        'id': p['poster-id'],
        'title': (pt := p.select('span.poster-title')[0].text.strip()),
        # We hash for faster(one pass) and consistent plain string merging
        # Also fixed length of hash makes string comparison faster compared to variable and lengthy paper name
        'hash': hashlib.md5(pt.encode('utf-8')).hexdigest(),
        'authors': [
            a.strip()
            for a in p.select('em')[0].text.replace(' and ', ',').split(',')  # fixme : use 'and' in split in re
            if len(a.strip()) > 0
        ],
        'session': sg.select('div.session-header')[0].text.strip(),  # fixme : Remove enclosing '()' brackets from text
        'sub_session': s.select('a.session-title')[0].text.strip(),  # todo : should it be renamed to Track?
        'weekday': (d := s.select('span.session-time')[0]['title'].split(','))[0].strip(),
        'date': d[1].strip(),
        'start_time': (t := s.select('span.session-time')[0].text.split('\u2013'))[0].strip(),
        'end_time': t[1].strip(),
        'url': p.select('i.fa-file-pdf-o')[0]['data'],
        'location': s.select('span.session-location')[0].text.strip().replace('\u2013', '-'),
    }
    for sg in soup.select('div.session-box')
    for s in sg.select('div.session')
    for p in s.select('table.poster-table tr#poster')
]

with open('posters.json', 'w') as outfile:
    json.dump(fn_poster_list, outfile, indent=2)

sorted_poster_list = sorted(fn_poster_list, key=lambda x: x['hash'])

validate_unique_hash(sorted_poster_list, 'session poster list from interactive schedule.')

check_for_duplicates(sorted_session_paper_list, sorted_poster_list, 'Session papers', 'Poster papers', True)

fuzzy_check_for_duplicates(sorted_session_paper_list, sorted_poster_list, 'Session papers', 'Poster papers', True)

with open('sorted_poster_list_iSchedule_sessions.json', 'w') as outfile:
    json.dump(sorted_poster_list, outfile, indent=2)

print("Matching posters of two lists .....")

# Sorting Unmerged Accepted paper list after fuzzy merging with session papers
unmatched_paper_list_after_fuzzy_merge.sort(key=lambda x: x['hash'])

# First apply plain string merging and reduce list
merged_poster_list, unmatched_poster_list, unmatched_poster_list2 \
    = merge_list(unmatched_paper_list_after_fuzzy_merge, sorted_poster_list)

with open('no_match_poster_list.json', 'w') as outfile:
    json.dump(unmatched_poster_list, outfile, indent=2)

with open('no_match_poster_list2.json', 'w') as outfile:
    json.dump(unmatched_poster_list2, outfile, indent=2)

with open('merged_poster_list.json', 'w') as outfile:
    json.dump(merged_poster_list, outfile, indent=2)

# Finally apply fuzzy merging to already reduced list
fuzzy_merged_poster_list, unmatched_paper_list_after_fuzzy_merge, unmatched_session_paper_list_after_fuzzy_merge \
    = fuzzy_merge_list(unmatched_poster_list, unmatched_poster_list2, True)

with open('no_match_poster_list_after_fuzzy_merge.json', 'w') as outfile:
    json.dump(unmatched_paper_list_after_fuzzy_merge, outfile, indent=2)

with open('no_match_poster_list2_after_fuzzy_merge.json', 'w') as outfile:
    json.dump(unmatched_session_paper_list_after_fuzzy_merge, outfile, indent=2)

with open('fuzzy_merged_poster_list.json', 'w') as outfile:
    json.dump(fuzzy_merged_poster_list, outfile, indent=2)

with open('emnlp-ijcnlp2019-Accepted-Papers-scrapper_data_func.txt', 'w') as outfile:
    json.dump(fn_paper_list, outfile, indent=2)
