from selenium import webdriver
import time
from openpyxl import Workbook
import pandas as pd
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import requests

# 엑셀시트 생성
wb = Workbook(write_only=True)
ws = wb.create_sheet()

# 인스타그램 사이트 오픈
# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.get("https://www.instagram.com/")
# driver.implicitly_wait(3)

# # 로그인
# driver.find_element_by_css_selector("#loginForm > div > div:nth-child(1) > div > label > input").send_keys("rhrlwld@gmail.com")
# driver.find_element_by_css_selector("#loginForm > div > div:nth-child(2) > div > label > input").send_keys("rkdals!234")
# driver.find_element_by_css_selector("#loginForm > div > div:nth-child(3) > button > div").click()
# time.sleep(3)

# ## 여기서 문제 발생!!!!


# # 팝업 종료
# driver.find_element_by_css_selector("#react-root > section > main > div > div > div > div > button").click()
# driver.find_element_by_css_selector("body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm").click()
# time.sleep(2)

# # 계정 접근
# insta_name = driver.find_element_by_css_selector("#react-root > section > nav > div._8MQSO.Cx7Bp > div > div > div.LWmhU._0aCwM > input")
# insta_name.send_keys('maru._.camping')
# time.sleep(2)

# insta_name.send_keys(Keys.ENTER)
# insta_name.send_keys(Keys.ENTER)
# time.sleep(2)




user_name = "maru._.camping"
url = f"http://www.instagram.com/{user_name}"   # username으로 url 생성

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
time.sleep(3)

# 첫번째 게시물 클릭
# N번째 게시물
driver.find_elements_by_css_selector('._9AhH0')[2].click()
time.sleep(1)

# 댓글 플러스 버튼 누르기
while True:
    try:
        button = driver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > div.EtaWk > ul > li > div > button > span')
    except:
        pass

    if button is not None:
        try:
            driver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > div.EtaWk > ul > li > div > button > span').click()
        except:
            break

# 대댓글 버튼 누르기
buttons = driver.find_elements_by_css_selector('li > ul > li > div > button')

for button in buttons:
    button.send_keys(Keys.ENTER)
    
    # 댓글 플러스 버튼 누르기
while True:
    try:
        button = driver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > div.EtaWk > ul > li > div > button > span')
    except:
        pass

    if button is not None:
        try:
            driver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > div.EtaWk > ul > li > div > button > span').click()
        except:
            break

# 대댓글 버튼 누르기
buttons = driver.find_elements_by_css_selector('li > ul > li > div > button')

for button in buttons:
    button.send_keys(Keys.ENTER)