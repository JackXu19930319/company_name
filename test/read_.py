import os

import pandas as pd

# 获取当前工作目录
current_directory = os.getcwd()

# 获取当前工作目录下所有文件
all_files = [file for file in os.listdir(current_directory) if file.endswith('.xlsx')]

# 遍历每个文件并读取
for file in all_files:
    file_path = os.path.join(current_directory, file)

    # 使用pandas的read_excel函数读取Excel文件
    df = pd.read_excel(file_path)

    # 打印数据框的前几行，以确保成功读取
    for index, row in df.iterrows():
        print(row['名稱'])
