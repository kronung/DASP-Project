"""Crawler to collect the EMNLP 2019 submission deadlines/important dates """
__author__ = "Yuqing_Xu"


from urllib import request
from bs4 import BeautifulSoup
import json
import logging

logger = logging.getLogger("submission_deadlines_crawler")

def extract_submission_deadlines(smd_url):
    """
    Extracts all information available for submission important dates at
    https://www.emnlp-ijcnlp2019.org/calls/papers .
    :return: a list of a dictionaries with a deadline represented as one dictionary.
    """
    logger.info('Start crawling SUBMISSION DEADLINES...')
    logger.info('Crawling data from: %s', smd_url)
    submission_deadlines = []
    try:
        page = request.urlopen(smd_url)
    except:
        logger.warning("URl could not be crawled!")
        return submission_deadlines

    soup = BeautifulSoup(page, 'html.parser')

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
    logger.info('Crawling SUBMISSION DEADLINES DONE')
    return(submission_deadlines)



