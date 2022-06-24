from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import time
import re

driver = webdriver.Chrome()
## webdriver

url = "http://www.instagram.com/accounts/login/"
## url for accessing

driver.get(url)
## open the site

time.sleep(3)
## wait for the page to fully open

# Log in
ID = str(input("아이디를 입력하세요 : "))
Passwd = str(input("비밀번호를 입력하세요 : "))

inputid = driver.find_element(By.NAME, 'username')
#inputid = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
#inputid.clear()
##first method is to find ID component by how web named the input textfield
##second method(hidden) is to find ID component by html tag

inputid.send_keys(ID)
print('sucess: id')

inputPw = driver.find_element(By.NAME, 'password')
#inputPw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
#inputPw.clear()
## first method is to find password component by how web named the input textfield
## second method(hidden) is to find password component by html tag

inputPw.send_keys(Passwd)
print('sucess: pw')

time.sleep(2)
## wait for the site to input given info

login_ok_button = driver.find_element(By.CSS_SELECTOR, ".sqdOP.L3NKy.y3zKF     ")
## find the html tag for log in button

login_ok_button.click()
## take action on the button

time.sleep(3)
print('sucess: login')
## wait for the site to fully log in