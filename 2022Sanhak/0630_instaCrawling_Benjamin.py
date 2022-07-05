import requests
from datetime import datetime
import json
import pandas as pd
from sqlalchemy import false

# 인스타그램의 API는 로그인 정보가 필요하므로
# 먼저 로그인을 진행한 후 사용
class Instagram:    
    def __init__(self): 
        self.csrf_token = "" 
        self.session_id = ""
        self.headers = {}
        self.cookies = {} # cookie : HTTP에서 사용자의 정보를 저장하는 데이터

        self.sess = None # 로그인 유지를 위해 requests의 session 클래스를 사용
        
    def login(self, username, password): # 인스타그램 로그인
        link = 'https://www.instagram.com/accounts/login/'
        login_url = 'https://www.instagram.com/accounts/login/ajax/'

        self.sess = requests.session()

        time = int(datetime.now().timestamp()) 
        response = self.sess.get(link) 
        csrf = response.cookies['csrftoken'] 
        
        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        self.headers = {
            # "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            # 특정 User-Agent를 사용하지 않으면 에러를 반환
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken": csrf
        }

        login_response = self.sess.post(login_url, data=payload, headers=self.headers)
        json_data = json.loads(login_response.text)

        print("**print login_response.status_code, login_response.text:**")
        print(login_response.status_code, login_response.text)

        # 토큰 등 로그인 정보를 받아온 후 cookies 변수에 저장
        if json_data["authenticated"]:
            self.cookies = login_response.cookies
        else:
            print("login failed ", login_response.text)



    def get_search_data_tag_name(self, tag_name): # 해쉬태그를 검색하여 나오는 게시물 정보
        url = "https://i.instagram.com/api/v1/tags/web_info"

        r = self.sess.get(
            url,
            headers=self.headers,
            cookies=self.cookies,
            params={
                "tag_name": tag_name
            }
        )

        return r.json()["data"]

    def get_top_search_tag(self, tag_name): # 인스타그램 검색창에 입력 시 실행되는 api, 추천 검색어를 반환함
        url = "https://www.instagram.com/web/search/topsearch/"

        r = self.sess.get(
            url,
            headers=self.headers,
            cookies=self.cookies,
            params={
                "context": "blended",
                "query": tag_name,
                "include_reel": "true"
            }
        )

        return r.json()["hashtags"]


username = "ID"
password = "PW"

instagram = Instagram()
instagram.login(username, password)

# 리스트 선언
top_post_username = []
top_post_like_count = []
top_post_comment_count = []

top_post = []
recent_post = []

recent_post_username = []
recent_post_like_count = []
recent_post_comment_count = []

# 해시태그 검색
tags = instagram.get_top_search_tag("#골프")

## 해시태그 추천 리스트
for tag in tags:
    print(tag["hashtag"]["name"])

print("")
print("** 해당 해시태그의 인기 게시글 정보를 출력합니다. **")

# 해시태그 검색
hashtag_search = instagram.get_search_data_tag_name("골프웨어")

## 해시태그 검색 페이지에서 데이터 크롤링(인기 게시글)
for i in range(0, 3):
    for j in range(0, 3):
        
        #계정명
        # top_post_username.append(hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"]["user"]["username"])
        # print("계정명 :", end= " ")
        # print(hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"]["user"]["username"])

        # 좋아요 수
        # top_post_like_count.append(hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"]["like_count"])
        # print("좋아요 수 :", end= " ")
        # print(hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"]["like_count"])

        # 댓글 수
        # top_post_comment_count.append(hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"]["comment_count"])
        # print("댓글 수 :", end= " ")
        # print(hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"]["comment_count"])


        top_username = hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"]["user"]["username"]
        top_like = hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"]["like_count"]
        top_comments = hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"]["comment_count"]
        
        top_post.append([top_username, top_like, top_comments])
        
        
        print("i: " + str(i) + " j: " + str(j))
        print('top_post_username: ')
        print(top_post_username)
        print("")
    

    
print("top_post의 값을 나타냅니다.")
print(top_post)

print("** 해당 해시태그의 최근 게시글 정보를 출력합니다. **")
print("")
## 해시태그 검색 페이지에서 데이터 크롤링(최근 게시글)
for i in range(0, 6):
    for j in range(0, 3):
        
        # print("행 : " + i + " 열 : " + j)
        # 계정명
        # recent_post_username.append(hashtag_search["recent"]["sections"][i]["layout_content"]["medias"][j]["media"]["user"]["username"])
        # print("계정명 :", end= " ")
        # print(hashtag_search["recent"]["sections"][i]["layout_content"]["medias"][j]["media"]["user"]["username"])
        
        # 좋아요 수
        # recent_post_like_count.append(hashtag_search["recent"]["sections"][i]["layout_content"]["medias"][j]["media"]["like_count"])
        # print("좋아요 수 :", end= " ")
        # print(hashtag_search["recent"]["sections"][i]["layout_content"]["medias"][j]["media"]["like_count"])
        
        # 댓글 수
        # recent_post_comment_count.append(hashtag_search["recent"]["sections"][i]["layout_content"]["medias"][j]["media"]["comment_count"])
        # print("댓글 수 :", end= " ")
        # print(hashtag_search["recent"]["sections"][i]["layout_content"]["medias"][j]["media"]["comment_count"])
    
        recent_username = hashtag_search["recent"]["sections"][i]["layout_content"]["medias"][j]["media"]["user"]["username"]
        recent_like = hashtag_search["recent"]["sections"][i]["layout_content"]["medias"][j]["media"]["like_count"]
        recent_comments = hashtag_search["recent"]["sections"][i]["layout_content"]["medias"][j]["media"]["comment_count"]
        
        recent_post.append(recent_username, recent_like, recent_comments)

        
## CSV 파일 저장
output_top = pd.DataFrame(top_post, columns=['username', 'like', 'comments'])
output_top.to_csv('top_post_9_v3.csv', index= False, encoding= 'cp949')

output_recent = pd.DataFrame(recent_post, columns=['username', 'like', 'comments'])
output_recent.to_csv('recent_post_18_v3.csv', index= False, encoding= 'cp949')

''' 아론
temp = pd.read_excel("data_tag_top.xlsx")
temp.drop(['Unnamed: 0'], axis=3, inplace= True)

tempy = pd.concat([temp, pd.DataFrame(csv_list_top, columns= ['username', 'like', 'comments'])])
tempy.to_excel("data_tag_top.xlsx")
'''