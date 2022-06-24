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
from webdriver_manager.chrome import ChromeDriverManager
import requests


user_name = "maru._.camping"
url = f"http://www.instagram.com/{user_name}"   # username으로 url 생성

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
time.sleep(3)

r = requests.get(url, params={"__a": 1, "__d": "dis"})  # requests로 GET 요청 보냄, params 파라미터로 path parameter 넣을 수 있음.

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