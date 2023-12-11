import json
import os
import random
import sys
import time
from datetime import datetime

from requests_html import HTMLSession

import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

import pandas as pd

from faker import Faker

fake = Faker()

session = HTMLSession()

read_data = []

area_list = []


def w_log(new_log_message):
    # 获取当前日期和时间
    now = datetime.now()
    # 格式化为字符串，例如：2023-01-12_14-30-45.txt
    formatted_datetime = now.strftime("%Y-%m-%d")
    filename = f"{formatted_datetime}.txt"
    with open(filename, 'a') as file:
        # 遍历新的日志信息并追加到文件
        file.write(new_log_message + '\n')


def w_excel(file, df1):
    output = 'output'
    # 获取当前工作目录
    current_directory = os.getcwd()
    # 构建文件路径
    output_directory = os.path.join(current_directory, output)
    excel_file_path = os.path.join(current_directory, output, file)
    # 创建目录
    os.makedirs(output_directory, exist_ok=True)

    # 检查文件是否存在
    if not os.path.exists(excel_file_path):
        # 如果文件不存在，使用 Pandas 创建一个新的 Excel 文件
        # 这里可以写入 DataFrame 中的数据，或者在后续步骤中写入
        df = pd.DataFrame(df1)

        # 将数据写入 Excel 文件
        df.to_excel(excel_file_path, index=False)

    # 使用 ExcelWriter 对象，并设置 mode='a'（append）模式
    with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a') as writer:
        # 将每个数据框写入 Excel 文件，指定 sheet_name
        df1.to_excel(writer, sheet_name='Sheet1', index=False)
        # df2.to_excel(writer, sheet_name='Sheet2', index=False)


def read_excel(file_path):
    # 使用pandas的read_excel函数读取Excel文件
    df = pd.read_excel(file_path)
    return df

    # # 打印数据框的前几行，以确保成功读取
    # for index, row in df.iterrows():
    #     data = {
    #         'index': index,
    #         'row': row,
    #     }
    #     read_data.append(data)


def request(method, url, **kwargs):
    for i in range(3):
        try:
            res = session.request(method, url, **kwargs)
            time.sleep(0.5)
            return res
        except:
            time.sleep(1)
            continue
    sys.exit('request error')


def get_area_list():
    res = request('get', 'https://104.cht.com.tw/WebAP/Query.aspx')
    if len(area_list) > 0:
        return area_list
    for area in res.html.find('area'):
        area_list.append({'code': area.attrs['code'], 'area': area.attrs['alt']})
    return area_list


def get_params():
    res = request('get', 'https://104.cht.com.tw/WebAP/Query.aspx')
    __VIEWSTATE = res.html.find('#__VIEWSTATE', first=True).attrs['value']
    __VIEWSTATEGENERATOR = res.html.find('#__VIEWSTATEGENERATOR', first=True).attrs['value']
    return __VIEWSTATE, __VIEWSTATEGENERATOR


def e_zeor(keyword):
    status = False
    Phone = None
    area_list = get_area_list()
    url = "https://104.cht.com.tw/WebAP/Query.aspx"
    for area in area_list:
        __VIEWSTATE, __VIEWSTATEGENERATOR = get_params()
        payload = {
            'oneScriptManager': 'oneScriptManager|btnSend',
            '__VIEWSTATEENCRYPTED': '',
            '__ASYNCPOST': 'true',
            'btnSend': '搜尋',
            'txtName': keyword,
            'cityList': area['area'],
            'ddlarea': area['code'],
            'hidcode': area['code'],
            '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            '__VIEWSTATE': __VIEWSTATE,
        }
        search_page = request('post', url, data=payload)
        for i in search_page.html.find('td'):
            Name = i.find('div.Name', first=True)
            Phone = i.find('div.Phone', first=True)
            if Name and Phone:
                status = True
                w_log_update(keyword, Phone, url)
                return status, Phone
    w_log_update(keyword, Phone, url)
    return status, Phone


def find_company(name):
    headers = {
        'User-Agent': fake.user_agent(),
    }
    status = False
    phone = None
    url = 'https://www.findcompany.com.tw'
    page = requests.get(url + '/%s' % name, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    if '登記電話' in soup.text:
        try:
            phone = soup.find('table', class_='d-none d-md-table mt-3 table table-bordered font-15').find_all('tr')[3].find_all('td')[1].text.replace(' ', '').strip()
            status = True
        except:
            pass
    w_log_update(name, phone, url)
    return status, phone


def archi(name):
    headers = {
        'User-Agent': fake.user_agent(),
    }
    status = False
    phone = None
    url = 'https://www.archi.net.tw/tw/yelpage/company.asp'
    page = requests.get(url + '?cate=&vcusarea2=0&vkeyword=%s' % name, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    items = soup.find_all('div', class_='item')
    for i in items:
        c_name = i.find('a').get('title')
        if c_name == name:
            phone = i.find('div', class_='contact').find_all('li')[1].find('a').get('title').replace('tel:', '').replace(' ', '').strip()
            status = True
    w_log_update(name, phone, url)
    return status, phone


def zhupiter(name):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36'}
    # headers = {
    #     'User-Agent': fake.user_agent(),
    # }
    status = False
    phone = None
    cse_token = None
    cselibVersion = None
    url = 'https://cse.google.com/cse.js?cx=partner-pub-4027255886607766:3055970085'
    pre_page = requests.get(url, headers=headers)
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
    page = requests.get(main_url, headers=headers)
    tmp_str = page.text
    tmp_str = tmp_str.replace('/*O_o*/', '').replace('google.search.cse.api7132(', '').replace(');', '')
    print(tmp_str)
    json_obj = json.loads(tmp_str)
    if 'results' in json_obj.keys():
        for i in range(0, len(json_obj['results'])):
            ogTitle = json_obj['results'][i]['richSnippet']['metatags']['ogTitle']
            if name in ogTitle and '電話' in ogTitle:
                phone = ogTitle.split('電話')[1].split('|')[0]
                status = True
                break
    w_log_update(name, phone, url)
    return status, phone


def w_log_update(name, phone, url):
    if phone is None:
        msg = url + '>>not find[%s]' % name
    else:
        msg = url + '>>[%s] get phone is [%s]' % (name, phone)
    w_log(msg)


def execute(df):
    # 获取总行数
    total_rows = len(df)
    # 创建 tqdm 进度条
    for index, value in tqdm(df.iterrows(), total=total_rows, desc='Processing', unit='row'):
        name = value.get('名稱')
        phone = value.get('名稱')
        if str(name) == 'nan' or str(name) == '':
            continue
        if str(phone) != 'nan' and len(str(phone)) > 8:
            continue
        phone = None
        status, phone = find_company(name)
        if status:
            # 更新 '電話' 列的值
            df.at[index, '電話'] = phone
        if phone is None:
            status, phone = archi(name)
            if status:
                # 更新 '電話' 列的值
                df.at[index, '電話'] = phone
        if phone is None:
            status, phone = e_zeor(name)
            if status:
                # 更新 '電話' 列的值
                df.at[index, '電話'] = phone
        if phone is None:
            status, phone = zhupiter(name)
            if status:
                # 更新 '電話' 列的值
                df.at[index, '電話'] = phone
        pause_time = random.uniform(3, 9)
        time.sleep(pause_time)
    return df


if __name__ == '__main__':
    # 获取当前工作目录
    current_directory = os.getcwd()
    # 获取当前工作目录下所有文件
    all_files = [file for file in os.listdir(current_directory) if file.endswith('.xlsx')]
    # 遍历每个文件并读取
    for file in all_files:
        file_path = os.path.join(current_directory, file)
        df = read_excel(file_path)
        print('%s 開始' % file)
        df_data = execute(df)
        # 将更新后的数据框写回 Excel 文件
        df_data.to_excel(file_path, index=True)
