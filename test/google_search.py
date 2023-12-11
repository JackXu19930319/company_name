import re
import sys
import time

from googlesearch import search
from bs4 import BeautifulSoup
import requests
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
    sys.exit('request error')


def google_search(query, num_results=10):
    results = []

    # 迭代指定數量的搜索結果
    for result in search(query, num_results=num_results):
        results.append(result)

    return results


def get_search_results_content(url):
    try:
        # 發送請求獲取頁面內容
        response = requests.get(url)
        response.raise_for_status()

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取頁面內容
        content = soup.get_text()
        return content

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content: {e}")
        return None


if __name__ == "__main__":
    phone_number = None
    headers = {
        'User-Agent': fake.user_agent()
    }
    # 輸入搜索查詢
    search_query = "光盛木業股份有限公司 電話"

    # 獲取搜索結果
    search_results = google_search(search_query)

    # 輸出搜索結果的內容
    for idx, result in enumerate(search_results, start=1):
        print(result)
        content = get_page('get', result, headers=headers)
        soup = BeautifulSoup(content.text, 'html.parser')
        # 提取頁面內容
        content = soup.get_text()
        if content is None:
            continue
        if "電話" in content:
            # 定义电话号码的正则表达式模式
            phone_pattern = re.compile(r'\d{2}-\d{8}')
            # 使用 findall 函数查找所有匹配的电话号码
            phone_numbers = phone_pattern.findall(content)
            if phone_numbers:
                print("找到的电话号码：")
                for phone_number in phone_numbers:
                    print(phone_number)
                    break
            if phone_number is not None:
                break
