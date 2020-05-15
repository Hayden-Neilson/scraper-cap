from flask import Flask, render_template
import requests
import psycopg2
import sys
import bs4
from bs4 import BeautifulSoup
from inflection import titleize


import pandas as pd 
import time
import urllib.request
from bs4 import BeautifulSoup


conn = psycopg2.connect(
            dbname = "Capstone",
            user = "postgres",
            password = "Hneilson1",
            host = "localhost"
)

cur = conn.cursor()







URL = "https://www.indeed.com/jobs?q=junior+web+developer&l=utah"   

soup = BeautifulSoup(urllib.request.urlopen(URL).read(), 'lxml')

results = soup.find_all('div', attrs={'data-tn-component': 'organicJob'})

job_val = ''
company_val = ''
salary_val = ''


for suggestion in results:


    job = suggestion.find('a', attrs={'data-tn-element': "jobTitle"})
    if job:
        print('job:', job.text.strip())
        job_val = job.text.strip()

    company = suggestion.find('span', attrs={"class":"company"})
    if company:
        print('company:', company.text.strip())
        company_val = company.text.strip()

    salary = suggestion.find('span',attrs={"class":"salaryText"})
    if salary:
        print("salaryText:", salary.text.strip())
        salary_val = salary.text.strip() 


    cur.execute("""INSERT INTO scraped_info (job, company, salary) VALUES('{}', '{}', '{}' );""".format(job_val, company_val, salary_val  )),
   
    conn.commit()
        
    
cur.close()

conn.close()