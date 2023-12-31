import sys
import time

import requests
from bs4 import BeautifulSoup
from faker import Faker

fake = Faker()


def get_page(method, url, **kwargs):
    e = ""
    res = None
    for i in range(3):
        try:
            if method == 'get':
                res = requests.get(url, **kwargs)
            elif method == 'post':
                res = requests.post(url, **kwargs)
            time.sleep(0.5)
            if res is None:
                sys.exit('request error')
            return res
        except Exception as e:
            time.sleep(1)
            continue
    raise e


def twincn(number):
    phone = None
    status = False
    try:
        headers = {
            'User-Agent': fake.user_agent(),
            "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": "Chromium;v=104,  Not A;Brand;v=99, Google Chrome;v=104",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "macOS",
            "sec-fetch-dest": "image",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-origin",
            "x-client-data": "CI+2yQEIprbJAQipncoBCJShywE=",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
        url = f'https://www.twincn.com/item.aspx?no={number}'
        page = get_page('get', url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        if soup.find('div', class_='table-responsive') is not None:
            tables = soup.find('div', class_='table-responsive').find_all('tr')
            for t in tables:
                if "電話" in t.text:
                    phone = t.find_all('td')[1].find_all('p')[0].text.split('(來源')[0].strip()
                    status = True
    except Exception as e:
        msg = f"twincn: {e}"
        print(msg)
    return status, phone


if __name__ == '__main__':
    print(twincn('43696296'))
