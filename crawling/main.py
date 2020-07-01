#-*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from multiprocessing import Pool
from Crawler import Crawler, Review
import time
import re
import csv
import os

def createCSV(review):#수집된 리뷰 데이터(Review 클래스)를 csv 파일로 변환
    print("CSV 쓰기 중")
    dir = re.sub(":|/"," ", review.getTitle())
    try:
        with open("Reviews/"+dir +".csv", "w", encoding='utf-8', newline='') as file:
            csvWriter = csv.writer(file)
            csvWriter.writerow(["내용", "평점", "공감수", "작성일"])
            for rev in review.reviews:                           
                csvWriter.writerow(rev)
    except Exception as e:
        print(e)
    print("CSV 쓰기 종료")

def getReviews(url):
    crawler = Crawler()
    review = crawler.find_reviews(url)
    if(review is not None):
        createCSV(review)   

def read_urlList(file_path):
    url_List = []
    with open(file_path, 'r', encoding='utf-8') as file:
        url_List = file.readlines()
    url_List = [item for item in url_List if item[0]!='#']
    return url_List

def main():
    urlList = read_urlList("urlList.txt")#수집할 게임의 리뷰 URL 목록
    n = 4
    pool = Pool(processes = n)#프로세스 n개를 사용해 다중 크롤링 수행
    pool.map(getReviews, urlList)
    pool.close()
    pool.join()
            
if __name__=="__main__":
    main()

