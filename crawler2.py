from playwright.sync_api import sync_playwright
import pandas as pd
import os
from datetime import datetime

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.kopo.ac.kr/jungsu/content.do?menu=247")
    
    
    # 요일 가져오기
    pwDays = page.query_selector_all(".menu tbody tr td:nth-child(1)")[:5]        
    dates = []
    days = []
    for day in pwDays:
        date, day = day.inner_text().replace('\n', ' ').split()
        dates.append(date)
        days.append(day)

    # 메뉴 가져오기 + 요일 병합
    pwMenus = page.query_selector_all(".menu td span")[:15]
    menus = []
    for idx,menu in enumerate(pwMenus):
        if idx%3==0: 
            menus.append(dates[idx//3])
            menus.append(days[idx//3])
        menu = menu.inner_text().replace('\r', '')
        menus.append(menu)  
                

    browser.close()
    
menus = [menus[i:i+5] for i in range(0,len(menus), 5)]


df = pd.DataFrame(menus, columns=["날짜", "요일", "조식", "중식", "석식"])

if os.path.exists("menus.xlsx"):
    today = str(datetime.today().date())
    pre_df = pd.read_excel("menus.xlsx")    
    if pre_df["날짜"].str.contains(today).any():
        print("이미 크롤링한 날짜입니다.")  
        exit()
    df = pd.concat([pre_df, df])

df.to_excel("menus.xlsx", index=False)