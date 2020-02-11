__author__ = "Samaun Ibna Faiz"

from pyquery import PyQuery as pq
from urllib import request

source = pq(url='https://www.emnlp-ijcnlp2019.org/program/accepted/',
            opener=lambda url, **kw: request.urlopen(url))
doc = source('section.page__content')

paper_list = []
for e in doc('h2'):
    for p in doc('h2 ~ ul li'):
        authors = []

        for a in pq(p)('i').text().replace(' and ', ',').split(','):
            if len(author := a.strip()) > 0:
                authors.append(author)

        paper_list.append({
            'title': pq(p)('span').text().strip() + '.',
            'authors': authors,
            'type': pq(e).text()
        })

print(paper_list)