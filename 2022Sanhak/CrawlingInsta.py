from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver          # webdriver 사용 이유 : 인스타는 자바스크립트로 짜여짐 
import time
import requests
import shutil

# https://www.instagram.com/explore/tags/%EC%95%84%EC%9D%B4%EC%9C%A0/

baseUrl = 'https://www.instagram.com/explore/tags/'
plusUrl = input('검색할 태그를 입력하세요 : ')
url = baseUrl + quote_plus(plusUrl)            # quote_plus : 한글로 입력한 값을 url로 변환해줌

print(url)

driver = webdriver.Chrome()
driver.get(url)

time.sleep(3)

# 원하는 태그를 입력해 그 페이지를 가져올 수 있게 됨 -> 이제는 그 페이지를 분석할 것임
html = driver.page_source
soup = BeautifulSoup(html)

imglist = []

# 스크롤 내리는 반복회수
for i in range(0, 5): 
    
    insta = soup.select('.v1Nh3.kIKUG._bz0w')   # 클래스가 3개 -> 중간 공백마다 .으로 표시해줘야함 (클래스를 가져올때는 앞에 . 붙여줘야함!)
    


    for i in insta:
        print('https://instgram.com' + i.a['href'])
        imgUrl = i.select_one('.KL4Bh').img['src']      # 한개만 가져올거라서 select_one, img 태그 중 src 부분만 가져옴
        imglist.append(imgUrl)
        imglist = list(set(imglist))
        html = driver.page_source
        soup = BeautifulSoup(html)
        insta = soup.select('.v1Nh3.kIKUG._bz0w')
            
    driver.execute_script("window.scrollTo(1, document.body.scrollHeight);")
    time.sleep(2)
    
n = 0

# 읽어온 이미지를 저장하는 행위를 반복하는 횟수
for i in range(0, 60):  
    # This is the image url.
    image_url = imglist[n] 
    # Open the url image, set stream to True, this will return the stream content.
    resp = requests.get(image_url, stream=True)
    # Open a local file with wb(write binary) permission
    local_file = open('./img/' + plusUrl + str(n) + '.jpg', 'wb')
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    resp.raw.decode_content = True
    # Copy the response stream raw data to local image file.
    shutil.copyfileobj(resp.raw, local_file)
    # Remove the image url response object.
    n += 1
    del resp
    
driver.close()

