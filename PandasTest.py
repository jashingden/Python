# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 17:57:59 2017

@author: eddyteng
"""
#from datetime import datetime, timedelta
#from pandas_datareader import data as web
#
#end = datetime.today()
#start = end - timedelta(days=20)
#df = web.DataReader('2330.tw', 'yahoo', start, end)
#
#df["Close"].plot()


import pandas as pd
import numpy as np
import csv

#df = pd.read_csv('D:\MITAKE\VSProject\MitakePortfolio\GPHONE_MTK.csv',
#        sep='\t', names=['PID', 'Org', 'UserID', 'Stocks', 'SN', 'HID', 'UpdateDT'])
#
#df.head()
#
#df['Stocks'].iloc[3].split('@')[2]

def get_k(stk):
    o = stk[:,3]
    o = o.astype(np.float)
    h = stk[:,4]
    h = h.astype(np.float)
    l = stk[:,5]
    l = l.astype(np.float)
    c = stk[:,6]
    c = c.astype(np.float)
    return [o, h, l, c]

def get_corrc(k1, k2):
    o = round(np.corrcoef(k1[0], k2[0])[0][1], 3)
    h = round(np.corrcoef(k1[1], k2[1])[0][1], 3)
    l = round(np.corrcoef(k1[2], k2[2])[0][1], 3)
    c = round(np.corrcoef(k1[3], k2[3])[0][1], 3)
    corrc = (o + h + l + c) / 4
    return corrc

def saveCSV(path, mylist):
    file = open(path, 'w', newline='')
    writer = csv.writer(file)
    writer.writerows(mylist)

def showChart(stk_sort):
    idx = 0
    for info in stk_sort:
        idx += 1
        if idx > 10:
            break
        end = int(info[2]) + 1
        start = end - comp_len
        stk = all_stock[start:end]
        close = stk[:,6]
        close = close.astype(np.float)
        name = info[0] + ':  ' + str(round(float(info[3]) * 100, 2)) + '%'
        df = pd.DataFrame(close, columns=[name])
        df.plot()

in_file = 'D:\MITAKE\VSProject\MitakeSmartV2\Project\deploy\DailyK_20210104.csv'
out_file = 'D:\MITAKE\VSProject\MitakeSmartV2\Project\deploy\SimilarK_20210104.csv'

all_stock = pd.read_csv(in_file, header=1, dtype='str')
all_stock = np.array(all_stock)

all_id = all_stock[:,0]
base_id = '6488'
stk_info = []
stk_id = ''
base_idx = 0
k_len = 1000
comp_len = 100
info = []

for i in range(len(all_id)):
    if stk_id != all_id[i]:
        if len(info) > 0:
            stk_info.append(info)
        stk_id = all_id[i]
        info = [stk_id, i, i, 0.0]
        if stk_id == base_id:
            base_idx = len(stk_info)
    else:
        info[2] = i

if len(info) > 0:
    stk_info.append(info)

base_info = stk_info[base_idx]
end = base_info[2] + 1
start = end - comp_len
stk_base = all_stock[start:end]
k_base = get_k(stk_base)

for info in stk_info:
    end = info[2] + 1
    start = end - comp_len
    if start >= info[1]:
        stk = all_stock[start:end]
        k = get_k(stk)
        info[3] = get_corrc(k_base, k)

stk_sort = np.array(stk_info)
sort = stk_sort[:,3]
sort = sort.astype(np.float)
stk_sort = stk_sort[np.argsort(sort)][::-1]

#saveCSV(out_file, stk_sort)
showChart(stk_sort)
