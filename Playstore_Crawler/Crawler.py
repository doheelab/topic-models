#-*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup

import time
import re

class Review(object):
    def __init__(self, title = '', grade = 0, development = '', genre = ''):
        self.title = title
        self.grade = grade
        self.development = development
        self.genre = genre
        self.reviews = []
    
    def getTitle(self):
        return self.title
    def getGrade(self):
        return self.grade
    def getReviews(self):
        return self.reviews
    def addReview(self, rev):
        self.reviews.append(rev)

class Crawler(object):
    def __init__(self, path_driver = './chromedriver'):
        options = webdriver.ChromeOptions()      
        options.add_argument('headless')# 창 없이 수행
        options.add_argument("disable-gpu")
        options.add_argument('window-size=1920x1080')
        options.add_argument('lang=ko_KR')#크롬 환경을 한글로 설정
        #options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3163.100 Safari/537.36")
        #크롬 드라이버 옵션 설정
        self.driver = webdriver.Chrome(executable_path=path_driver, chrome_options=options)
        #self.wordDic = list()

    def find_reviews(self, url, minLen = 20):
        #인자: URL, 리뷰 최소 길이
        #역활: url을 인자로 받아 minLen 길이보다 긴 리뷰들이 저장된 Review 클래스를 Return   
        self.driver.get(url)
        self.driver.implicitly_wait(3)#웹 페이지를 불러올 때 3초간 기다림

        successTime = 0
        errTime = 0
        page = ''
        while(True):#스크롤바 첫 버튼 발견할 때까지 내림
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.implicitly_wait(0.5)
            try:                                         
                element = self.driver.find_element_by_xpath('//div[@class="U26fgb O0WRkf oG5Srb C0oVfc n9lfJ"]')
                if(element is not None):
                    element.click()
                    break
            except Exception:
                continue

        while(errTime < 30 and successTime < 20):#더보기 버튼을 20번 누를 때 까지 반복
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.implicitly_wait(0.05)
            try:                                    
                element = self.driver.find_element_by_xpath('//div[@class="U26fgb O0WRkf oG5Srb C0oVfc n9lfJ M9Bg4d"]') 
                if(element is not None):
                    element.click()
                    successTime+=1
                    errTime = 0#더보기 버튼이 눌러지면 errTime을 0으로 초기화
                    page = self.driver.page_source
            except Exception:
                errTime += 1
        try:
            page = self.driver.page_source
        except Exception:
            print('오류...')

        self.driver.quit()#크롬 드라이버 종료
        print("리뷰 동적 페이지 수집 끝")
        try:
            #reviews = driver.find_elements_by_xpath("//div[@class='UD7Dzf'] | //div[@class='xKpxId zc7KVe']")
            bsObj = BeautifulSoup(page, "lxml")

            #제목, 개발사, 장르 추출
            title = bsObj.find("h1", {"class": "AHFaub"}).get_text()
            development = bsObj.find("span", {"class":"T32cc UAO9ie"}).get_text()
            genre = bsObj.find("a", {"itemprop":"genre"}).get_text()

            #평점 추출
            grade = bsObj.find('div',{"role":"img"}).get('aria-label')
            star = re.findall(r"\d*\.\d+|\d+", grade)

            #리뷰 클래스 생성
            review_ = Review(title = title, grade = float(star[1]), development=development, genre = genre)

            #리뷰 수집 시작
            div_reviews = bsObj.find_all("div", {"class":"d15Mdf bAhLNe"})
            print(" %s 리뷰 수집 시작" % title)

            for div in div_reviews:
                grade = div.find('div',{"role":"img"}).get('aria-label')
                star = re.findall(r"\d*\.\d+|\d+", grade)#평점

                date_ = div.find('span', {"class":"p2TkOb"}).get_text()
                t = re.findall(r"\d*\.\d+|\d+", date_)
                date = '{0}-{1}-{2}'.format(t[0], t[1], t[2])#작성일

                good = div.find('div', {"class":"jUL89d y92BAb"}).get_text()#공감수

                content = div.find('span', {"jsname":"bN97Pc"}).get_text()
                content = content.replace("전체 리뷰", "")           
                content = re.sub('[^가-힝0-9a-zA-Z_!?@#%^&-=:;,\"\'<>\\s]', '', content)
                content.encode('utf-8')#리뷰 내용
            
                if(len(content) > minLen):#길이가 minLen 이상인 리뷰만 수집
                    review_.addReview((content, float(star[1]), int(good), date))
        except Exception as e:
            print(e)
        #리뷰 수집 끝
        print("리뷰 수: " + str(len(review_.reviews)))
        return review_