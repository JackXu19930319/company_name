import os
import random
import time

import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

import pandas as pd

from faker import Faker

fake = Faker()

read_data = []


def w_log(new_log_message):
    with open('log.txt', 'a') as file:
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


def find_company(name):
    headers = {
        'User-Agent': fake.user_agent(),
        # 'Accept-Language': fake.language_code(),
        # 'Referer': fake.url(),
        # 'Accept-Encoding': fake.random_element(elements=('gzip', 'deflate')),
        # 'Connection': fake.random_element(elements=('keep-alive', 'close')),
        # 可根据需要添加其他头部信息
    }
    status = False
    msg = ''
    phone = None
    # print('https://www.findcompany.com.tw/ >>start find[%s]' % name)
    url = 'https://www.findcompany.com.tw/%s'
    page = requests.get(url % name, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    if '登記電話' in soup.text:
        try:
            phone = soup.find('table', class_='d-none d-md-table mt-3 table table-bordered font-15').find_all('tr')[3].find_all('td')[1].text.replace(' ', '').strip()
        except:
            msg = 'https://www.findcompany.com.tw/ <<<<Error有「登記電話」字串，但卻噴錯>>>>'
    if phone is None:
        msg = 'https://www.findcompany.com.tw/ >>not find[%s]' % name
        status = False
        # print('https://www.findcompany.com.tw/ >>not find[%s]' % name)
    else:
        msg = 'https://www.findcompany.com.tw/ >>[%s] get phone is [%s]' % (name, phone)
        status = True
    w_log(msg)
    # print(msg)
    return status, phone


def execute(df):
    # 获取总行数
    total_rows = len(df)
    # 创建 tqdm 进度条
    for index, value in tqdm(df.iterrows(), total=total_rows, desc='Processing', unit='row'):
        name = value.get('名稱')
        phone = value.get('名稱')
        # if str(phone) != 'nan' and len(str(phone)) > 8:
        #     continue
        status, phone = find_company(name)
        if status:
            # 更新 '電話' 列的值
            df.at[index, '電話'] = phone
            continue
        pause_time = random.uniform(2, 5)
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
