# Experimental Conference Crawler

This is a separate project for Experimentation. Some features were adapted to main
conference crawler project. Others might be adapted with adequate or no modification. 

**Please Note that**
* Contents inside should be treated as an independent project.
* Some of the scripts might need ```python 3.8```
* This project might have it's own library dependencies independent of the main project.
* DSL part is not fully implemented so there might only be som explanations of 
  concepts available(c.f. project report).
  
 ### Scripts included
 
* *naacl2019-Accepted-Papers-scrapper.py* 
    - Demonstrates the concept of Parent pre-processing and child pruning 
* *emnlp-ijcnlp2019-Accepted-Papers-scrapper.py* 
    - Demonstrates an experimental application of *fuzzy* merging
* *pyquery.py*
    - A sample usage of ``pyquery`` library on *emnlp* accepted papers
* *Emnlp.dsl*
    - An example dsl representation of crawling job description on *emnlp* accepted papers
* *acl2020.py*
    - A reference crawler for acl2020's important_dates, Accepted tutorials and Accepted Workshops
    
    