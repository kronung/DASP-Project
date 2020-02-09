"""Crawler to collect the NAACL2019, ACL2019, ACL2020, EMNLP2019 and COLING2020 organizers """
__author__ = "Yuqing Xu"


import requests
import bs4
from bs4 import BeautifulSoup
import json
import logging

logger = logging.getLogger("organizers_crawler")

def extract_organizers(organizers_url=None):
    """
     Extracts basic information available for organizers provided at
     the organization site of the conference (works for NAACL2019, ACL2019,
     ACL2020, EMNLP2019 and COLING2020).

     :param: organizers_url: the url where the papers are listed (default None)
             (for example https://naacl2019.org/organization )
     :return: list of dictionaries with organizers in a conference represented as one dictionary.
     """
    logger.info('Start crawling PAPERS...')
    organizers = []

    # crawl the papers site
    if organizers_url is not None:
        logger.info('Crawling data from: %s', organizers_url)
        try:
            page = requests.get(organizers_url)
        except:
            logger.warning("URl could not be crawled!")
            return organizers

    soup = BeautifulSoup(page.content, 'html.parser')

    # on the organizers sites, five conferences could be divided into two categories:
    # (1) With the text of "Organizing Committee" in the <h1> tag -- NAACL2019, ACL2020, EMNLP2019, and COLING2020
    # (2) With the text of "Committees" in the <h1> tag -- ACL2019
    if 'Organizing Committee' in soup.find('h1').text:
        # In this case, 4 conferences in (1) could be classified into two classes:
        # (3) has <h3> tags -- NAACL2019 and ACL2020
        # (4) has no <h3> tag -- COLING2020 and EMNLP2019

        if soup.find('h3') is not None:
            """crawling organizers for NAACL2019, ACL2020
            the structures of the organization page are same in NAACL2019 and ACL2020 """
            for child in soup.findChildren('section', {'class': 'page__content'}):
                for position in child.find_all('h3'):
                    organizer = {attribute: None for attribute in ['position', 'members']}
                    organizer['position'] = position.text.split('[')[0]
                    organizer['members'] = position.findNextSibling('p').text.replace('\n', ';')
                    organizers.append(organizer)


        elif soup.find('h5') is not None:
            # COLING2020 and EMNLP2019 have no <h3> tag, while the structures of them are different
            # these two conferences could be distinguished by <h5> tag:
            # (5) has <h5> tags -- COLING2020
            # (6) has no <h5> tag -- EMNLP2019

            """crawling organizers for COLING2020"""
            div = soup.find('section', {'class': 'page-section'})
            for child in div.find_all('div', {'class': 'col-lg-12'}):
                organizer = {attribute: None for attribute in ['position', 'members']}
                organizer['position'] = child.find('h2').text
                members = child.findNext('div', {'class': 'row'}).find_all('h5')
                organizer['members'] = []
                for m in members:
                    organizer['members'].append(m.text)
                organizers.append(organizer)

        else:
            """crawling organizers for EMNLP2019"""
            for child in soup.find_all('h2'):
                organizer = {attribute: None for attribute in ['position', 'members']}
                if child.findNextSibling().name == 'table':
                    organizer['position'] = child.text
                    organizer['members'] = []
                    for tr in child.findNextSibling('table').findChildren('tr'):
                        organizer['members'].append(
                            tr.find('td').findNextSibling('td').text.replace('\n', '').replace('\xa0', ''))
                    organizers.append(organizer)
                elif child.findNextSibling().name == 'p':
                    main_url = "https://www.emnlp-ijcnlp2019.org"
                    new_url = main_url + child.findNextSibling('p').find('a').get('href')
                    new_page = requests.get(new_url)
                    new_soup = BeautifulSoup(new_page.content, 'html.parser')
                    for child in new_soup.find('h2', id='area-chairs').findNextSibling('table').findChildren('tr'):
                        organizer['position'] = new_soup.find('h2', id='area-chairs').text + ': ' + child.find(
                            'td').findNextSibling('td').find('b').text
                        organizer['members'] = child.find('td').findNextSibling('td').text.split('\n')[1]
                        organizers.append(organizer)
                        organizer = {attribute: None for attribute in ['position', 'members']}

    else:
        """crawling organizers for ACL2019"""
        for child in soup.find("section", {"class": "content"}).find_all('p'):
            organizer = {attribute: None for attribute in ['position', 'members']}
            if child.find('strong') is not None:
                organizer['position'] = child.find('strong').get_text()
            if child.find('em') is not None:
                organizer['members'] = []
                for i in child.find_all('em'):
                    organizer['members'].append(i.text)
            organizers.append(organizer)

    return clear_organizers(organizers)

# clear the result if one of the attributes is none
def clear_organizers(org_list):
    for i in org_list:
        if i['position'] == None or i['members'] == []:
            org_list.remove(i)
    return org_list


#print(extract_organizers("https://naacl2019.org/organization"))
#print(extract_organizers("http://www.acl2019.org/EN/committees.xhtml"))
#print(extract_organizers("https://acl2020.org/organization"))
#print(extract_organizers("https://www.emnlp-ijcnlp2019.org/organization"))
#print(extract_organizers("https://coling2020.org/pages/organization"))