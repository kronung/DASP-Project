import json

import requests
from bs4 import BeautifulSoup, SoupStrainer, Tag

r = requests.get('https://naacl2019.org/program/accepted/')
html_doc = r.text

page_content = SoupStrainer('section', class_='page__content')
soup = BeautifulSoup(html_doc, 'html.parser', parse_only=page_content)


def is_proper_sibling(element: Tag, parent_next_sibling_line: int, parent_next_sibling_pos: int) -> bool:
    return (
               element.sourcepos - parent_next_sibling_pos
               if element.sourceline - parent_next_sibling_line == 0
               else element.sourceline - parent_next_sibling_line
           ) < 0


def find_next_sibling_line(element: Tag, tag_type: str) -> int:
    nxt_sib = element.find_next_sibling(tag_type)
    return float("inf") if nxt_sib is None else nxt_sib.sourceline


def find_next_sibling_position(element: Tag, tag_type: str) -> int:
    nxt_sib = element.find_next_sibling(tag_type)
    return float("inf") if nxt_sib is None else nxt_sib.sourcepos


fn_paper_list = {
    el['elem'].text:
        [
            {
                'title': p.strong.text.strip(),
                'authors': [
                    a.strip()
                    for a in p.strong.find_next_sibling(string=True).replace(' and ', ',').split(',')
                    if len(a.strip()) > 0
                ]
            }
            for p in el['elem'].find_all_next('p')
            if is_proper_sibling(p, el['nxt_sib_line'], el['nxt_sib_pos'])
        ]
    for el in [
        {
            'elem': e,
            'nxt_sib_line': find_next_sibling_line(e, 'h2'),
            'nxt_sib_pos': find_next_sibling_position(e, 'h2')
        }
        for e in soup.find_all('h2')
    ]
}

print(fn_paper_list)

# for debugging
# for key in fn_paper_list.keys():
#     total_papers = len(fn_paper_list[key])
#     fstPaper = fn_paper_list[key][0]
#     lstPaper = fn_paper_list[key][total_papers - 1]
#     print(key, total_papers, fstPaper, lstPaper)

with open('naacl2019-Accepted-Papers-scrapper_data_func.txt', 'w') as outfile:
    json.dump(fn_paper_list, outfile, indent=2)
