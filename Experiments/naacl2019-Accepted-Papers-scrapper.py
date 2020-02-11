__author__ = "Samaun Ibna Faiz"

import json
from urllib import request

from bs4 import BeautifulSoup, SoupStrainer

from util.util import pre_process_types, get_proper_siblings

################################################
# Accepted Paper list                          #
################################################

source = 'https://naacl2019.org/program/accepted/'

page_content = SoupStrainer('section', class_='page__content')
# page_content = SoupStrainer('section.page__content')
soup = BeautifulSoup(request.urlopen(source), 'html.parser', parse_only=page_content)


fn_paper_list = [
    {
        'title': p.strong.text.strip(),
        'authors': [
            a_
            for a in p.strong.find_next_sibling(string=True).replace(' and ', ',').split(',')
            if len((a_ := a.strip())) > 0
        ],
        'type': el['elem'].text
    }

    for el in pre_process_types(soup.find_all('h2'))  # Pre-processing of parent
    for p in get_proper_siblings(el, 'p')  # Pruning of improper siblings
]

print(json.dumps(fn_paper_list, indent=4))

# for key in fn_paper_list.keys():
#     total_papers = len(fn_paper_list[key])
#     fstPaper = fn_paper_list[key][0]
#     lstPaper = fn_paper_list[key][total_papers - 1]
#     print(key, total_papers, fstPaper, lstPaper)

# with open('naacl2019-Accepted-Papers-scrapper_data_func_modified2.txt', 'w') as outfile:
#     json.dump(fn_paper_list, outfile, indent=2)
