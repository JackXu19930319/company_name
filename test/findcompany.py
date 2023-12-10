import requests
from bs4 import BeautifulSoup

name = '台彰投資有限公司'

url = 'https://www.findcompany.com.tw/%s'
page = requests.get(url % name)
soup = BeautifulSoup(page.content, 'html.parser')
if '登記電話' in soup.text:
    print(soup)
# phone = soup.find('table', class_='d-none d-md-table mt-3 table table-bordered font-15').find_all('tr')[3].find_all('td')[1].text.replace(' ', '').strip()
