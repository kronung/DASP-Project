"""Crawler to collect the EMNLP 2019 submission deadlines/important dates """
__author__ = "Yuqing_Xu"


import requests
from bs4 import BeautifulSoup
import json

def extract_submission_deadlines(smd_url):
    """
       Extracts all information available for submission important dates at
       https://www.emnlp-ijcnlp2019.org/calls/papers .
       :return: a list of a dictionaries with a deadline represented as one dictionary.
       """
    page = requests.get(smd_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    submission_deadlines = []
    tables = soup.find_all('table')
    tab = tables[0].get_text()
    array1 = [i for i in tab.split('\n') if i != '']
    array2 = []
    [array2.append(array1[i:i+3]) for i in range(0,len(array1),3)]
    for i in array2:
        submission_deadline = {attribute: None for attribute in ["name", "datetime"]}
        submission_deadline['name'] = i[0]
        submission_deadline['datetime'] = i[2]
        submission_deadlines.append(submission_deadline)
    #print(json.dumps(submission_deadlines, indent=1))
    return(submission_deadlines)



