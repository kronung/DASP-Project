__author__ = "Samaun Ibna Faiz"

import json
from urllib import request
from bs4 import BeautifulSoup, SoupStrainer

################################################
# Important conference event dates/deadlines   #
################################################

source = 'https://acl2020.org/'

page_content = SoupStrainer('section', class_='page__content')
soup = BeautifulSoup(request.urlopen(source), 'html.parser', parse_only=page_content)

important_dates = [
    {
        'Event': (c := r.find_all('td'))[0].text,
        'day': c[1].text.replace('\u2013', '-'),
        'date': c[2].text.replace('\u2013', '-')
    }
    for r in soup.find('h2', {'id': 'dates'}).find_next_sibling('center').select('table tbody tr')
]

print(json.dumps(important_dates, indent=4))
################################################
# Accepted tutorials list                      #
################################################

source = 'https://acl2020.org/program/tutorials/'

page_content = SoupStrainer('section', class_='page__content')
soup = BeautifulSoup(request.urlopen(source), 'html.parser', parse_only=page_content)

tutorials = [
    {
        'title': t.text.strip(),
        'organizer': t.find_next_sibling('p').em.text
            .strip().replace('Organizers:', '').strip().replace(' and ', ', ').split(', '),
    }
    for t in soup.find_all('h3')
]

print(json.dumps(tutorials, indent=4))
################################################
# Accepted Workshop list                       #
################################################

source = 'https://acl2020.org/program/workshops/'

page_content = SoupStrainer('section', class_='page__content')
soup = BeautifulSoup(request.urlopen(source), 'html.parser', parse_only=page_content)

workshops = [
    {
        'title': wt.text,
        'description': (d := wt.find_next_sibling('p')).text.split('\n')[0].strip(),
        'organizer': d.em.text.replace('Organizers: ', '').replace(' and ', ', ').split(', '),
    }
    for wt in soup.find_all('h3')
]

print(json.dumps(workshops, indent=4))
