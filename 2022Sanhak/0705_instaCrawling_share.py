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

    def get_user_info(self, user_id): # 단일 계정에 대한 정보 반환
        url = "https://i.instagram.com/api/v1/users/web_profile_info"
        
        r = self.sess.get(
            url,
            headers=self.headers,
            cookies=self.cookies,
            params={
                "username": user_id
            }
        )
        
        return r.json()["data"]

username = "ID" 
password = "PW"

instagram = Instagram()
instagram.login(username, password)

# 리스트 선언
top_post = []
recent_post = []

# 해시태그 검색
tags = instagram.get_top_search_tag("#골프")

## 해시태그 추천 리스트
for tag in tags:
    print(tag["hashtag"]["name"])

while True:
    
    # 해시태그 검색
    hash_string = str(input("해시태그 입력 : "))
    hashtag_search = instagram.get_search_data_tag_name(hash_string)

    if hash_string == 'end':
        break

    else:
        
        ## 해시태그 검색 페이지에서 데이터 크롤링(인기 게시글)
        for i in range(0, 3):
            for j in range(0, 3):
        
                top_username = hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"]["user"]["username"]
                top_like = hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"]["like_count"]
                top_comments = hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"]["comment_count"]
        
                hashtag_top_user = instagram.get_user_info(top_username)
                
                top_follower = hashtag_top_user["user"]["edge_followed_by"]["count"]
                top_following = hashtag_top_user["user"]["edge_follow"]["count"]
                top_biography = hashtag_top_user["user"]["biography"]
                
                top_user_like = 0
                top_user_comments = 0
                
                for k in range(0, 12):
                    temp_like = hashtag_top_user["user"]["edge_owner_to_timeline_media"]["edges"][k]["node"]["edge_liked_by"]["count"]
                    top_user_like += temp_like
                    
                    temp_comments = hashtag_top_user["user"]["edge_owner_to_timeline_media"]["edges"][k]["node"]["edge_media_to_comment"]["count"]
                    top_user_comments += temp_comments
                    
                top_avglike = top_user_like / 12
                top_avgcomments = top_user_comments / 12
                top_ER = (top_avglike + top_avgcomments) / top_follower * 100

                top_post.append([hash_string, top_username, top_like, top_comments, top_follower, top_following, top_biography, top_avglike, top_avgcomments, top_ER])
        
        print("***** 인기 게시글 정보 수집 완료 *****")
        print("----- top post -----")
        print(top_post)
        print("")
       

        ## 해시태그 검색 페이지에서 데이터 크롤링(최근 게시글)
        for i in range(0, 6):
            for j in range(0, 3):
        
                recent_username = hashtag_search["recent"]["sections"][i]["layout_content"]["medias"][j]["media"]["user"]["username"]
                recent_like = hashtag_search["recent"]["sections"][i]["layout_content"]["medias"][j]["media"]["like_count"]
                recent_comments = hashtag_search["recent"]["sections"][i]["layout_content"]["medias"][j]["media"]["comment_count"]
                
                hashtag_recent_user = instagram.get_user_info(recent_username)
                
                recent_follower = hashtag_recent_user["user"]["edge_followed_by"]["count"]
                recent_following = hashtag_recent_user["user"]["edge_follow"]["count"]
                recent_biography = hashtag_recent_user["user"]["biography"]
                
                recent_user_like = 0
                recent_user_comments = 0
                
                for k in range(0, 12):
                    temp_like = hashtag_recent_user["user"]["edge_owner_to_timeline_media"]["edges"][k]["node"]["edge_liked_by"]["count"]
                    recent_user_like += temp_like
                    
                    temp_comments = hashtag_recent_user["user"]["edge_owner_to_timeline_media"]["edges"][k]["node"]["edge_media_to_comment"]["count"]
                    recent_user_comments += temp_comments
                    
                recent_avglike = recent_user_like / 12
                recent_avgcomments = recent_user_comments / 12
                recent_ER = (recent_avglike + recent_avgcomments) / recent_follower * 100
        
                recent_post.append([hash_string, recent_username, recent_like, recent_comments, recent_follower, recent_following, recent_biography, recent_avglike, recent_avgcomments, recent_ER])
        print("***** 최근 게시글 정보 수집 완료 *****")
        print("----- recent post -----")
        print(recent_post)
        print("")
        
## CSV 파일 저장
'''
부연설명
username : 계정명
like : 해시태그 검색창에서의 인기/최근 게시글의 좋아요 수
comments : 해시태그 검색창에서의 인기/최근 게시글의 좋아요 수
biography : 계정의 소개글
likeAvg : 해당 계정의 최근 12개 게시글에 대한 평균 좋아요 수
commentsAvg : 해당 계정의 최근 12개 게시글에 대한 평균 댓글 수
ER : 최근 12개 게시글에 대한 ER지수
'''
output_top = pd.DataFrame(top_post, columns=['hashtag', 'username', 'like', 'comments', 'follower', 'following', 'biography', 'likeAvg', 'commentsAvg', 'ER'])
output_top.to_csv('top_post_9_v9.csv', index= False, encoding= 'utf-8')

output_recent = pd.DataFrame(recent_post, columns=['hashtag','username', 'like', 'comments', 'follower', 'following', 'biography', 'likeAvg', 'commentsAvg', 'ER'])
output_recent.to_csv('recent_post_18_v9.csv', index= False, encoding= 'utf-8')
