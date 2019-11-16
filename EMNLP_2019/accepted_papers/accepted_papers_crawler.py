import json

import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.emnlp-ijcnlp2019.org/program/accepted/')
html_doc = r.text

soup = BeautifulSoup(html_doc, 'html.parser')

fn_paper_list = dict(
    (
        e.get_text(),
        [
            {
                'title': p.span.get_text().strip(),
                'authors': [
                    a.strip()
                    for a in p.i.get_text().replace(' and ', ',').split(',')
                    if len(a.strip()) > 0
                ]
            }
            for p in e.find_next_sibling('ul').find_all('li')
        ]
    )

    for e in soup.find_all('h2')
)

print(fn_paper_list)

with open('emnlp-ijcnlp2019-Accepted-Papers-scrapper_data_func.txt', 'w') as outfile:
    json.dump(fn_paper_list, outfile, indent=2)
