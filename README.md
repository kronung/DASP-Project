# DASP-Project

GitHub repo for our DASP project.
Add all your code here guys, so we can use the same data structure and stuff.

[Document](https://docs.google.com/document/d/1bVkfrczlRNVy4IZ4dJLEL9QZOCtYDooHd6jsqqGXRns/edit#
) with our goals for the project:

[The outline of project report](https://docs.google.com/document/d/14oZGG45kpDjZuAx0sWMc_y0m91utRmwA4CDJHmuqMUo/edit?usp=sharing
)

[First presentation](https://docs.google.com/presentation/d/15QHucPB7vOlxxqTh7_59tIPKPIw8nK8uY5EHov2GAXQ/edit#slide=id.g6e23f894b7_0_12)

## How to use the program:
--- confcrawler version 1.0 UKP Lab TU Darmstadt python3 ---
Confcrawler help instructions:
confcrawler lets you crawl data for specific nlp conference websites,
which have the same html template than emnlp2019 or naacl2019.
It tries to extract as much information as it can for the provided urls
to generate a conference.json file with the structured data.

####How to run the program:  
Open terminal, navigate to the root folder of the programm 'DASP-Project'  
Type via Terminal:  

```python3 confcrawler.py YOUR_FILEPATH_TO_CONF_FILE.TXT OUTPUT_FOLDER_FILEPATH```
  
####Parameter:
- CONF_FILE.txt - filepath to txt file of the form:  
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
only change the urls, not the the property names, if no url leave empty.
- OUTPUT_FOLFER_FILEPATH (optional, default output is saved to data folder of 
program)
