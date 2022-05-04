import json
import random
from collections import OrderedDict
import pandas as pd
import sys
import io
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from konlpy.tag import Hannanum
from pykospacing import Spacing
import re

def getSeverdata(answer_user):
    answer_df =pd.DataFrame(answer_user, index=[0])
    answer_df = answer_df[['director', 'genre', 'actors', 'grade', 'date']]
    
    nlpAnswer_list = []
    for i in range(3):
        new_answer = answer_df.loc[0][i].replace(" ",'')
        spacing=Spacing()
        kospacing_answer = spacing(new_answer)
        hannanum=Hannanum()
        a = hannanum.nouns(kospacing_answer)
        nlpAnswer_list.append(a)

    grade = answer_df.loc[0][3]
    year = answer_df.loc[0][4]

    if grade.find("전체") >= 0:
        grade_result = "전체"
    else:
        grade_result = re.sub(r'[^0-9]', '', grade)

    year_result = re.sub(r'[^0-9]', '', year)
    nlpAnswer_list.append(grade_result)
    nlpAnswer_list.append(year_result)
    #[['유선동'], ['공포','스릴러'], ['정은지'], '15', '2019']
    print(nlpAnswer_list)
    return nlpAnswer_list


def runningApp(answer_user): #메인
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8') #한글깨짐 방지
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8') #한글깨짐 방지

    #파이어베이스에서 데이터 가져오기
    db_url = 'https://chattingbot-86c46-default-rtdb.firebaseio.com/'
    cred = credentials.Certificate("c:\\projects\\Mudra\\chattingbot-86c46-firebase-adminsdk-41i2v-6c371d4648.json")
    default_app = firebase_admin.initialize_app(cred, {'databaseURL': db_url})
    df = pd.DataFrame(db.reference('한국영화').get())

    #사용자에게 받은 대답 리스트로 처리
    answer = getSeverdata(answer_user)

    # 예외처리하기.
    # 리스트 안에 값 2개 있을 시 따로 처리. 
    tmp = df[df['director'].str.contains(answer[0][0], na=False)]
    tmp = tmp[tmp['grade'].str.contains(answer[3], na=False) & tmp['genre'].str.contains(answer[1][0], na=False) 
    & tmp['actors'].str.contains(answer[2][0], na=False) & tmp['dates'].str.contains(answer[4], na=False)]
    name = tmp.iloc[0]['movie_name']
    return name


if __name__ == '__main__':
    answer_user = { #사용자에게 받은 대답( 안스에서 넘어온거 )
        'date' : '2019',
        'actors' : '정은지',
        'director' : '유선동',
        'grade' : '15',
        'genre' : '공포'
    }
    result = runningApp(answer_user)
    print(result)