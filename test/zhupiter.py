import json

import requests
from bs4 import BeautifulSoup

name = "萬旺企業行"
cse_token = None
cselibVersion = None
url = 'https://cse.google.com/cse.js?cx=partner-pub-4027255886607766:3055970085'
pre_page = requests.get(url)
for line in pre_page.text.splitlines():
    if '"cse_token":' in line:
        cse_token = line[:-1].replace('cse_token":', '').strip().replace('"', '')
        cse_token = str(cse_token).strip()
    elif '"cselibVersion":' in line:
        cselibVersion = line[:-1].replace('"cselibVersion":', '').strip().replace('"', '')
        cselibVersion = str(cselibVersion).strip()

if cse_token is None or cselibVersion is None:
    raise Exception('主網頁無法下載 : 無法取得授權碼')
main_url = 'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=zh-TW&source=gcsc&gss=.com&cx=partner-pub-4027255886607766:3055970085&safe=active&lr=&cr=&gl=&filter=0&sort=&as_oq=&as_sitesearch=&exp=csqr,cc&callback=google.search.cse.api7132'
main_url = main_url + '&cselibv=' + cselibVersion
main_url = main_url + '&q=' + name
main_url = main_url + '&cse_tok=' + cse_token

page = requests.get(main_url)
tmp_str = page.text
tmp_str = tmp_str.replace('/*O_o*/', '').replace('google.search.cse.api7132(', '').replace(');', '')
print(tmp_str)
json_obj = json.loads(tmp_str)
for i in range(0, len(json_obj['results'])):
    ogTitle = json_obj['results'][i]['richSnippet']['metatags']['ogTitle']
    if name in ogTitle and '電話' in ogTitle:
        phone = ogTitle.split('電話')[1].split('|')[0]
        print(phone)
        break
