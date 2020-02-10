# README DASP-Project
## Assisting with Information on NLP Conferences: Conference Website Crawler

This software is the result of the Data Analysis Software Project at TU Darmstadt 
offered by the UKP lab (2019/20).  
The problem: Multiple international NLP conferences every year. As mentioned in this 
blogpost [here](https://naacl2019.org/blog/digital-and-collaborative-materials/) the NLP
community tries to publish a uniform website structure for future NLP conferences. 
Unfortunately there is no API or uniform structure/ interface to collect the data of a 
conference. The data consist of information about the papers, tutorials, workshops, keynotes
and general information of a conference.    

Have a look at the following NLP conference websites:  
[NAACL 2019](https://naacl2019.org/)  
[EMNLP 2019](https://www.emnlp-ijcnlp2019.org/)  
[ACL 2020](https://acl2020.org/)
 
The above mentioned conferences follow the proposed website structure in the blogpost.
This software implements a crawler for websites of this structure. It lets you extract
detailed information on each conference entities (papers, tutorials etc.) and generates
json data files to store the crawled information.
It also includes a script to build a sql dump file from the generated json files.
The generated data can be used to feed the UKP Athena Chatbot with information
on NLP conferences.

## How to use the program: 
```confcrawler.py``` lets you crawl data for specific NLP conference websites,
which have the same html template than [NAACL 2019](https://naacl2019.org/) or
[EMNLP 2019](https://www.emnlp-ijcnlp2019.org/).
It tries to extract as much information as it can for the provided urls
to generate a conference.json file with the structured data. For more information
on the crawling process see part **Functionality**

**Required libraries: beautifulSoup4, requests** (check requirements.txt)  
For the json template structure see ```conference_template.json``` in the 
folder ```ressources```.

### How to run the crawler:  
Open terminal, navigate to the root folder of the program 'DASP-Project'  
Type via Terminal:  

```python3 confcrawler.py YOUR_FILEPATH_TO_CONF_FILE.TXT OUTPUT_FOLDER_FILEPATH```
  
#### Parameter:
- CONF_FILE.txt - filepath to txt file of the form (example NAACL 2019):  
```
conf_name = NAACL 2019
topics_url = 
organizers_url = 
schedule_url = https://naacl2019.org/schedule/
papers_url = https://naacl2019.org/program/accepted/
workshops_url = https://naacl2019.org/program/workshops/
tutorials_url = https://naacl2019.org/program/tutorials/
keynotes_url = https://naacl2019.org/program/keynotes/
smd_url = https://naacl2019.org/
```
Only change the urls, not the the property names, if no url leave empty.
Specify as much urls as you can identify on the website to increase the chance
of collecting all the available information.

- OUTPUT_FOLFER_FILEPATH (optional, default output is saved to **data** folder of 
program)

### How to generate SQL Dump from data files:
Lets you generate a sql dump file to create a sql database from the conference 
json data files. For the database scheme see ```db_scheme.txt``` in the 
folder ```ressources```.

Open terminal, navigate to the root folder of the program 'DASP-Project'  
Type via Terminal:  

```python3 create_database_dump.py YOUR_FILEPATH_TO_THE_DATA_FOLDER OUTPUT_FOLDER_FILEPATH```
#### Parameter:  
- THE_DATA_FOLDER - filepath to folder where the conference data files are stored:  
The folder must only contain .json data files of crawled conferences.  
Default folder DASP-Project --> data/ (needs to be specified in any case).

 - OUTPUT_FOLFER_FILEPATH (optional, default output is saved to sql folder of program)
 
 Example calls:  
 
          python3 create_database_dump.py data
          python3 create_database_dump.py data /user/folder1/folder2
          
## Functionality

## Crawler
Main crawler at  ```confcrawler -> conference_crawler.py``` which calls the
entity crawlers located at ```confcrawler -> universalcrawler -> crawler/``` . 
The crawler only works if the html structure corresponds to the expected one.  
For each entity (paper, tutorial, workshops, keynotes, organizers etc.)
we implemented one crawler. The following crawlers  
      
          keynote_crawler.py
          paper_crawler.py
          tutorial_crawler.py
          workshop_crawler.py
          
try to collect data from two locations (if specified via urls). First the entity 
page on the website ([paper entity example](https://naacl2019.org/program/accepted/))
and second the interactive schedule ([schedule example](https://naacl2019.org/schedule/)).
It then tries to merge the results together. This allows the user to crawl 
only by the entity page or the schedule page or both. Most of the time
there are optional information attributes available on one of the locations, so
to get the maximum data specify both urls.

**Warning**: If the html structure of specific parts differ from the expected one,
the crawler is not able to collect the data and needs to be adjusted.    

### Queries
It is possible to query the json data files:
To make some queries see   
```confcrawler -> queries -> queries.py``` documentation. 
These queries are only an interface, so that another python script can collect
specific information of the data file an further process it.

### Logging
The crawling process is logged to the console and to the logging file, 
which can be found at ```confcrawler -> logs -> confcrawler.log``` 

## Obtained Data
The obtained data consists of five conference data:  
  
**NAACL 2019**   
**ACL 2020**  
**EMNLP 2019**  
**COLING 2019**  
**ACL 2019**

The json data files can be found at   
```DASP-Project -> data``` folder.  

 

### Contact
Aron Kaufmann <kaufmann.aron@gmail.com>  
Lars Meister <meista95@googlemail.com>  
Samaun Ibna Faiz <samaun.xiii@gmail.com>  
Yuqing Xu <yuqingxu0506@163.com>
