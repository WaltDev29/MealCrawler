import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, timedelta

# requests
response = requests.get("https://www.kopo.ac.kr/jungsu/content.do?menu=247")
html = response.text


# parsing
soup = BeautifulSoup(html, "html.parser")
soupMenus = soup.select(".menu td span")[:15]
soupDays = soup.select(".menu tbody tr td:nth-child(1)")[:5]


# day, date
today = date.today()
days = []
for idx,soupDay in enumerate(soupDays):    
    day = soupDay.text
    days.append(f"{today + timedelta(days=idx)} {day}")
    
    
# menus
menus = []
for idx,soupMenu in enumerate(soupMenus):
    if idx%3==0:menus.append(days[idx//3])
    menu = soupMenu.text.strip().replace('\r','')    
    menus.append(menu)
menus = [menus[i:i+4] for i in range(0,len(menus),4)]


# DataFrame
df = pd.DataFrame(menus, columns=["구분","조식","중식","석식"])

# concat
if os.path.exists("menus.xlsx"):    
    pre_excel = pd.read_excel("menus.xlsx")
    df = pd.concat([pre_excel, df])

# to excel
df.to_excel("menus.xlsx", index=False)