import requests
from bs4 import BeautifulSoup

name = "元鎮室內裝修設計有限公司"

url = 'https://www.archi.net.tw/tw/yelpage/company.asp'
page = requests.get(url + '?cate=&vcusarea2=0&vkeyword=%s' % name)
soup = BeautifulSoup(page.content, 'html.parser')
items = soup.find_all('div', class_='item')
for i in items:
    c_name = i.find('a').get('title')
    if c_name == name:
        phone = i.find('div', class_='contact').find_all('li')[1].find('a').get('title').replace('tel:', '').replace(' ', '').strip()
        print(phone)
