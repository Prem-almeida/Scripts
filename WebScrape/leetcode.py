import requests
from bs4 import BeautifulSoup # use pip install bs4
import pandas as pd
import numpy as np
from selenium import webdriver # use pip3 install selenium
import time
import os
from datetime import date

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')#will Show you the browser in action

path = os.getcwd()
print ("The current working directory is %s" % path)

#please download the chromedriver according to the browser on your system and put the path below 
# download https://sites.google.com/a/chromium.org/chromedriver/home driver
driver = webdriver.Chrome(path+"/chromedriver")

path=(path+'/LeetCode/Data/')
print('make dir in '+path)

try: 
    os.makedirs(path, exist_ok = True) 
    print("Directory created successfully" ) 
except OSError as error: 
    print("Directory can not be created")

# Getting the website with all the issues noted 
# but since some fields are collapsed need to expand them
driver.get("https://leetcode.com/problemset/all/")
more_buttons = driver.find_elements_by_class_name("btn-round")

for x in range(len(more_buttons)):
      if more_buttons[x].is_displayed():
          driver.execute_script("arguments[0].click();", more_buttons[x])

time.sleep(5)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')


df = pd.DataFrame(columns = ['Company', 'questions','applied']) 




x=1
for company in soup.findAll('a',class_='lg-company'):
    print(x)
    x=x+1
    for badge in company.findAll('span',class_='badge'):
        badge1=(badge.text).strip()     
    for span in company.findAll('span',class_='text-gray'):
        company=(span.text).strip()
        # print("company: "+company+" badge: "+badge1+" ADDED LG")
        df = df.append({'Company' : company, 'questions' : badge1, 'applied' : 0},ignore_index = True)

for company in soup.findAll('a',class_='sm-company'):
    for badge in company.findAll('span',class_='badge'):
        badge1=(badge.text).strip()     
    for span in company.findAll('span',class_='text-gray'):
        company=(span.text).strip()
        # print("company: "+company+" badge: "+badge1+"ADDED SM")
        df = df.append({'Company' : company, 'questions' : badge1, 'applied' : 0},ignore_index = True)

driver.close()
# print(df)
today = date.today()
# today = today.strftime('%Y-%m-%d-%H:%M:%S')
size = len(path)

from pathlib import Path

path = Path(__file__).parent.absolute()
print(str(path) +'/Data/LeetCode'+str(today)+'_Companies_.csv')

df.to_csv(str(path) +'/Data/LeetCode_'+str(today)+'_Companies_.csv')