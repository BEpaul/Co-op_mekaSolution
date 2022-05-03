from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver              # webdriver 사용 이유 : 인스타는 자바스크립트로 짜여짐 
import time

# https://www.instagram.com/explore/tags/%EC%95%84%EC%9D%B4%EC%9C%A0/

baseUrl = 'https://www.instagram.com/explore/tags/'
plusUrl = input('검색할 태그를 입력하세요 : ')
url = baseUrl + quote_plus(plusUrl)         # quote_plus : 한글로 입력한 값을 url로 변환해줌

print(url)

driver = webdriver.Chrome()
driver.get(url)

time.sleep(3)

# 원하는 태그를 입력해 그 페이지를 가져올 수 있게 됨 -> 이제는 그 페이지를 분석할 것임
html = driver.page_source
soup = BeautifulSoup(html)

insta = soup.select('.v1Nh3.kIKUG._bz0w')       # 클래스가 3개 -> 중간 공백마다 .으로 표시해줘야함 (클래스를 가져올때는 앞에 . 붙여줘야함!)

n = 1

for i in insta:
    print('https://instgram.com' + i.a['href'])
    imgUrl = i.select_one('.KL4Bh').img['src']     # 한개만 가져올거라서 select_one, img 태그 중 src 부분만 가져옴
    with urlopen(imgUrl) as f:
        with open('./img/' + plusUrl + str(n) + '.jpg', 'wb') as h:     # str() : 정수나 실수를 문자열로 바꾸어주는 내장 함수
            img = f.read()
            h.write(img)
            
    n += 1
    print(imgUrl)
    print()
    
    
driver.close()