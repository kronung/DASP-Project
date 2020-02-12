# README DASP-Project
## Assisting with Information on NLP Conferences: Conference Website Crawler

This software is the result of the Data Analysis Software Project at TU Darmstadt 
offered by the UKP lab (2019/20).  
The problem: Multiple international NLP conferences every year. As mentioned in this 
blogpost [here](https://naacl2019.org/blog/digital-and-collaborative-materials/) the NLP
community tries to publish a uniform website structure for future NLP conferences. 
Unfortunately there is no API or uniform structure/ interface to collect the data of a 
conference. The data consists of information about the papers, tutorials, workshops, keynotes
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
- **CONF_FILE.txt** - filepath to txt file of the form (example NAACL 2019):  
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

- **OUTPUT_FOLFER_FILEPATH** (optional, default output is saved to **data** folder of 
program)  

Example call:  

```python3 confcrawler.py conf_urls_emnlp19.txt```


### How to generate SQL Dump from data files:
Lets you generate a sql dump file to create a sql database from the conference 
json data files. For the database scheme see ```db_scheme.txt``` in the 
folder ```ressources```.

Open terminal, navigate to the root folder of the program 'DASP-Project'  
Type via Terminal:  

```python3 create_database_dump.py YOUR_FILEPATH_TO_THE_DATA_FOLDER OUTPUT_FOLDER_FILEPATH```
#### Parameter:  
- **THE_DATA_FOLDER** - filepath to folder where the conference data files are stored:  
The folder must only contain .json data files of crawled conferences.  
Default folder DASP-Project --> data/ (needs to be specified in any case).

 - **OUTPUT_FOLFER_FILEPATH** (optional, default output is saved to sql folder of program)
 
 Example calls:  
 
          python3 create_database_dump.py data
          python3 create_database_dump.py data /user/folder1/folder2
          
## Functionality

### Crawler
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

#### Merging Mechanism:
For the main entites (papers, workshops, tutorials, keynotes) two data locations can be identified.
The entity crawlers reflect this fact and offer two specify these two locations.    
In the end we have to merge the results of these two data locations together.  
This is done by the following priority: 
 1. Preprocess the titles and authors (string cleaning, lower-casing etc.) 
 2. **Match titles** (paper_title, tutorial_name, keynote_title, workshop_name)  
    If no match:  
 3. **Match authors** (only in case of papers and tutorials)   
 
 If no match is found we create a new entity entry (then we say they are different).  
 For some reasons sometimes the same entity has two different titles in the entity page and the 
 interactive schedule, therefore we matching the authors as well. But in special cases even that 
 is not enough, therefore some entities get two entries in the final json data file. (The 
 question is when are two papers for example actually the same?)    
 **Statistic**: NAACL 19: 38 / 511 not matching -> 7.4 %
 
 **Note**:  
 The matching can be extended to do fuzzy matching or substring matching, but keep in mind that 
 you increase the chance to merge two originally different entities into one and therefore loose 
 data by those strategies.
 We decided to go with the explained approach!

#### How to add new entities to the crawler:
One can easily add new entities. Just add the new entity to the JSON 
template (new property with corresponding attributes) and call your crawler in the main crawler. 
Keep in mind that your crawler must return a list and the attributes must correspond 
to the attributes in the template.

#### How to extend/adjust existing entity crawler:
If you want to adjust an existing crawler, e.g ```paper_crawler.py```, because a new website
structure has been published (sometimes differences can be very small in the DOM) try to find
a unique determiner which differentiate this new HTML structure from the existing one.
Then add a new if clause to the crawler based on that determiner, where you extract your desired 
data fields from the DOM. If you want to merge the data with the schedule data include a 
reference dictionary (sometimes two), where you store the merging data field (in case of the paper 
crawler this will be the cleaned title and the cleaned authors). Always check the documentation 
in the entity crawler to understand how this specific crawler works.   
 
**Keep in mind**:   
We tried to make the crawler as robust as possible to handle different conferences. In our case 
we had two examples (NAACL 2019 and EMNLP 2019), which had quiet some differences in their 
sepcific form of the DOM, although they both used the proposed uniform HTML template mentioned in 
the blogpost. Obviously, we have no influence on how future conferences website publisher will 
publish their specific form of that website template, therefore it is hard for any general 
crawler to prepare for a future case. Therefore it could be necessary to adjust the crawler or 
write a new entity.     
     

### Queries
It is possible to query the json data files:
To make some queries see   
```confcrawler -> queries -> queries.py``` documentation. 
These queries are only an interface, so that another python script can collect
specific information of the data file an further process it.

### SQL Database scheme
For a figure of the database scheme see final report.  
```data.sql``` script tested on MySQL Workbench.  

#### How to change the database sheme:
```ressources -> db_scheme.txt```  
Change table declarations, datatypes and relations.  
Afterwards adjust the ```craete_database_dump.py``` script:  
Change the INSERT statements in the```read_file()``` function to fit your needs. 

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

 

## Contact
Aron Kaufmann <kaufmann.aron@gmail.com>  
Lars Meister <meista95@googlemail.com>  
Samaun Ibna Faiz <samaun.xiii@gmail.com>  
Yuqing Xu <yuqingxu0506@163.com>
