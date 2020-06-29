#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 10:17:16 2020

@author: dohee
"""

#%%

# read HTML

from bs4 import BeautifulSoup
import requests

url = 'https://play.google.com/store/apps/details?id=com.nexon.v4kr&showAllReviews=true'
html = requests.get(url)
bs0bj = BeautifulSoup(html.text, 'lxml')

div_reviews = bs0bj.find_all("div", {"class":"zc7KVe"})#"d15Mdf bAhLNe"
#%%

from bs4 import BeautifulSoup
from selenium import webdriver

# read Xml (Playstore)
url = 'https://play.google.com/store/apps/details?id=com.nexon.v4kr&showAllReviews=true'

driver = webdriver.Chrome(executable_path = '/home/dohee/kaggle/recommend/chromedriver')
driver.get(url)
html = driver.page_source
driver.quit()

bs0bj = BeautifulSoup(html, 'lxml')

div_reviews = bs0bj.find_all("div", {"class":"zc7KVe"})
print(len(div_reviews))

#%%

# read Xml (Playstore)

from bs4 import BeautifulSoup
from selenium import webdriver
import time

url = 'https://play.google.com/store/apps/details?id=com.nexon.v4kr&hl=ko&showAllReviews=true'

driver = webdriver.Chrome(executable_path = '/home/dohee/kaggle/recommend/chromedriver')
driver.get(url)
driver.implicitly_wait(3)

cnt = 0
while(cnt<10): # scroll down 10 times
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    cnt += 1
    time.sleep(0.5)
html = driver.page_source
driver.quit()

bs0bj = BeautifulSoup(html, 'lxml')
div_reviews = bs0bj.find_all("div", {"class":"zc7KVe"})
print(len(div_reviews))

#%% 

# "more" button

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import csv 


def crawling(url):

    #url = 'https://play.google.com/store/apps/details?id=com.nexon.v4kr&hl=ko&showAllReviews=true'
    
    driver = webdriver.Chrome(executable_path = '/home/dohee/kaggle/recommend/chromedriver')
    driver.get(url)
    driver.implicitly_wait(3)
    # until finding the first "more" button
    while(True): 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        
        try:
            # find button
            element = driver.find_element_by_xpath('//div[@class="U26fgb O0WRkf oG5Srb C0oVfc n9lfJ"]')
            if (element is not None):
                element.click()
                break
        except:
            continue
    
    errTime = 0
    successTime = 0
    
    # until finding the next "more" button
    
    while (errTime<20 and successTime < 2):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.05)
        try:
            element = driver.find_element_by_xpath('//div[@class="U26fgb O0WRkf oG5Srb C0oVfc n9lfJ M9Bg4d"]')
            if (element is not None):
                element.click()
                successTime+=1
                errTime = 0 # initialize if the botton is found
        except Exception:
            errTime += 1
    
    html = driver.page_source
    driver.quit()
    
    
    bs0bj = BeautifulSoup(html, 'lxml')
    div_reviews = bs0bj.find_all("div", {"class":"zc7KVe"})
    print(len(div_reviews))            
            
    reviews = []
        
    for div in div_reviews:
        try:
            grade = len(div.find_all('div', {'class':'vQHuPe bUWb7c'}))
            date_ = div.find('span', {"class":"p2TkOb"}).get_text()
            t = re.findall(r"\d*\.\d+|\d+", date_)
            date= '{0}-{1}-{2}'.format(t[0], t[1], t[2]) # date
            good = div.find('div', {"class":"jUL89d y92BAb"}).get_text()
            content = div.find('span', {"jsname":"bN97Pc"}).get_text()
            content = content.replace("전체 리뷰", "")
            content = re.sub('[;]', '', content)
            #content = re.sub('[^가-힝0-9a-zA-Z_!?@#%^&-=:;,\"\'<>\\s]', '', content)
            content.encode('utf-8') # review

            reviews.append((content, grade, good, date))
            #content = content.replace("")
        except:
            pass
    
    with open("review.csv", 'wt', encoding = 'utf-8', newline='') as file:
        csvWriter = csv.writer(file)
        csvWriter.writerow(["내용", "평점", "공감수", "작성일"])
        for rev in reviews:
            csvWriter.writerow(rev)


#%%


from multiprocessing import Pool


url = 'https://play.google.com/store/apps/details?id=com.nexon.v4kr&hl=ko&showAllReviews=true'
urlList = [url]
n = 4
pool = Pool(processes = n)
pool.map(crawling, urlList)

#%%

# 단어 빈도수 분석
    
import os 
import pandas as pd

def searchFiles(path):
    filelist = []
    filenames = os.listdir(path)
    for filename in filenames:
        file_path = os.path.join(path, filename)
        filelist.append(file_path)
    return filelist

def main():
    reviews = []
    for filePath in searchFiles(r'/home/dohee/kaggle/recommend/'):
        if filePath[-3:]=='csv':
            review = pd.read_csv(filePath, encoding = 'utf-8')
            reviews.append(review)
    docs = pd.concat(reviews, ignore_index=True)
    return docs
    
if __name__=="__main__":
    docs = main()
    
#%%
    




