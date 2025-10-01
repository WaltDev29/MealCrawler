import os
import pandas as pd
from datetime import datetime

if not os.path.exists("menus.xlsx"):
    print("파일이 존재하지 않습니다.")
    print("크롤링을 먼저 진행해주세요\n")
    input("아무 키나 눌러 종료")
    exit()

file = pd.read_excel("menus.xlsx")

weekdays = ["월요일","화요일","수요일","목요일","금요일","토요일","일요일"]
weekday = weekdays[datetime.today().weekday()]
today = str(datetime.today().date())

if not file["구분"].str.contains(today).any():
    print("오늘 날짜 학식 정보가 없습니다.")
    print("크롤링을 먼저 진행해주세요\n")
    input("아무 키나 눌러 종료")
    exit()
    
todayMenus = file[file["구분"].str.contains(today, na=False)]
print(f"=== 오늘의 학식 ===")
print(today, weekday, end='\n\n')
print(f"--- 조식 ---\n{todayMenus["조식"].to_string(index=False)}\n")
print(f"--- 중식 ---\n{todayMenus["중식"].to_string(index=False)}\n")
print(f"--- 석식 ---\n{todayMenus["석식"].to_string(index=False)}\n")
input("아무 키나 눌러 종료")