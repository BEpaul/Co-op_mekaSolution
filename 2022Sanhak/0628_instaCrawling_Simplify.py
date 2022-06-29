from pyparsing import col
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time
import re
from sqlalchemy import true
from webdriver_manager.chrome import ChromeDriverManager
import requests

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

## 01. 웹 열기
driver = webdriver.Chrome(ChromeDriverManager().install()) #웹드라이버로 크롬 웹 켜기
driver.set_window_size(800, 1200) 	#브라우저 크기 800*1200으로 고정
driver.get('https://www.instagram.com/') #인스타그램 웹 켜기
time.sleep(2) 	#2초 대기

## 02. 로그인
#경로 지정
id_box = driver.find_element_by_css_selector("#loginForm > div > div:nth-child(1) > div > label > input")   #아이디 입력창
password_box = driver.find_element_by_css_selector("#loginForm > div > div:nth-child(2) > div > label > input")     #비밀번호 입력창
login_button = driver.find_element_by_css_selector('#loginForm > div > div:nth-child(3) > button')      #로그인 버튼

#동작 제어
act = ActionChains(driver)      #동작 명령어 지정
act.send_keys_to_element(id_box, 'rhrlwld@gmail.com').send_keys_to_element(password_box, 'rkdals!234').click(login_button).perform()     #아이디 입력, 비밀 번호 입력, 로그인 버튼 클릭 수행
time.sleep(2)

#저정할 리스트 선언
crawling_data = []

while true:
    
    ## 03. 계정 검색
    user = str(input("Search for the user: "))
    
    if user == 'end':
        break
    
    else:
        
        profile = "http://www.instagram.com/" + str(user)
        driver.get(profile)
        time.sleep(5)

        ## 04. 계정주 정보 수집

        r = requests.get(profile, params={"__a": 1, "__d": "dis"})  # requests로 GET 요청 보냄, params 파라미터로 path parameter 넣을 수 있음.

        # 반환된 JSON 데이터(r)을 .json() 메소드로 파이썬에서 사용할 수 있는 dict 형식으로 변경


        # 반환 데이터에서 "graphql"키와 "user"키에서 유저 데이터를 담고 있는것을 확인하였으므로 변수에 저장함
        user_data = r.json()["graphql"]["user"]

        engine_category = r.json()["seo_category_infos"]

        # dict에서 필요한 데이터 가져옴
        intro = user_data["biography"]
        name = user_data["full_name"]
        follower = user_data["edge_followed_by"]["count"]
        following = user_data["edge_follow"]["count"]

        print(engine_category)
        print(intro)
        print(name)
        print(follower)
        print(following)
        
        crawling_data.append([engine_category, intro, name, follower, following])
        

        
output = pd.DataFrame(crawling_data, columns=['category', 'intro', 'name', 'follower', 'following']) 
output.to_csv('crawlingData.csv', index = False, encoding='cp949')    