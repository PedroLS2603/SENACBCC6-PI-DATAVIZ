import pandas as pd
import numpy as np
import os
import re

dfs = []

files = os.listdir(os.path.join(os.getcwd(), "data/"))

files.sort()

for file in os.listdir(os.path.join(os.getcwd(), "data/")):
    df = pd.read_csv(os.path.join(os.getcwd(), "data/",file), dtype="string")

    if len(file) == 14 and file.__contains__("13."):
        cp_file = file[:9] + '0' + file[9]  + file[10:]
        df['patch'] = cp_file.replace('patch_', '').replace('.csv', '')
    elif len(file) == 14 and file.__contains__(".2"):
        cp_file = file[:6] + '0' + file[6]  + file[7:]
        df['patch'] = cp_file.replace('patch_', '').replace('.csv', '')

    df['region'] = df['region'].replace('EUNE', 'EU')
    df['region'] = df['region'].replace('EUW', 'EU')

    df['region'] = df['region'].replace('LAS', 'LA')
    df['region'] = df['region'].replace('LAN', 'LA')

    dfs.append(df)

concat = pd.concat(dfs)
concat = concat[concat['region'] != '']
concat = concat[concat['role'] != '']
concat.to_csv("consolidada.csv", encoding="utf-8")
concat.to_csv("consolidada 2.csv", encoding="utf-8")
