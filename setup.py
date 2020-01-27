#!/usr/bin/env python3
from setuptools import setup

setup(
   name='confcrawler',
   version='1.0',
   description='A module to crawl nlp conference data',
   author='Aron Kaufmann, Lars Meister, Samaun Ibna Faiz, Yuqing Xu',
   packages=['confcrawler'],  #same as name
   install_requires=['beautifulSoup4', 'requests', 'python-dateutil'],
   entry_points={
       'console_scripts':  [
           'confcrawler=confcrawler:run'
       ]
   }

)