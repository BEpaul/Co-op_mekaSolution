from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re                                                # 정규표현식 사용하기 위해
import pandas as pd                                      # pandas : 데이터분석 라이브러리

driver = webdriver.Chrome("chromedriver")                # webdriver 사용, url 가져옴
url = "http://www.instagram.com/accounts/login/"
driver.get(url)
time.sleep(3)


## 1. Login 

user_id = str(input("아이디를 입력하세요 : "))             # id, password String으로 변환
user_passwd = str(input("비밀번호를 입력하세요 : "))

instagram_id_form = driver.find_element_by_name('username')
instagram_id_form.send_keys(user_id)
print('sucess: id')

instagram_pw_form = driver.find_element_by_name('password')
instagram_pw_form.send_keys(user_passwd)
print('sucess: pw')

time.sleep(2)
      
login_ok_button = driver.find_element_by_css_selector(".sqdOP.L3NKy.y3zKF     ")        
login_ok_button.click()
time.sleep(3)
print('sucess: login')


## 2. Get information function

def getContent(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')                                  # 페이지 소스인 html python으로 parsing

    # content
    try:
        content = soup.select('div.MOdxS')[0].text                              #게시글 내용 수집
    except:
        content = None

    # tag
    instagram_tags = []
    try:
        data = driver.find_element_by_css_selector(".C7I1f.X7jCj")                   # tag 수집
        tag_raw = data.text
        tags = re.findall('#[A-Za-z0-9가-힣]+', tag_raw)                          # settin tag format (정규표현식 이용)
        tag = ''.join(tags).replace("#"," ")

        tag_data = tag.split()                                                    # tag split 후 list에 추가

        for tag_one in tag_data:
            instagram_tags.append(tag_one)
    except:
        pass
     
    # date
    try:
        date = soup.select('time._1o9PC')[0]['title']
    except:
        date = None

    # like
    try:
        like = soup.select('section.EDfFK.ygqzn')[0].findAll('span')[-1].text
    except:
        like = None

    # location
    try:
        place = soup.select('div.M30cS')[0].text
    except:
        place = None

    data = [content, date, like, place, instagram_tags]
    print(data)
    return data



## 3. Hashtag Searching & crawling

result = []         # 결과값 담을 list 생성

while True:
    
    keyword = str(input("검색어를 입력하세요 : "))

    if keyword == '##stop##':   # 해당 키워드 입력하면 크롤링 종료
        break
    else:
        hashtag_url = "http://www.instagram.com/explore/tags/" + str(keyword)
        driver.get(hashtag_url)
        time.sleep(5)

        first = driver.find_element_by_css_selector('.v1Nh3.kIKUG._bz0w')       
        first.click()
        time.sleep(3)


        for i in range(10):                 # 10개의 게시글에 대해 Crawling 진행
            result.append(getContent(driver))

            right = driver.find_element_by_css_selector("div.l8mY4.feth3")
            right.click()
            time.sleep(2)


result_df = pd.DataFrame(result, columns = ['content', 'date', 'like', 'place', 'tags'])
result_df.to_csv('./instagram_crawling.csv')    # 크롤링 파일 저장















