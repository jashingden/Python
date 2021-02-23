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

def showChart(all_stock, stk_sort, comp_len):
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

def readDailyK(in_file, base_id):
    all_stock = pd.read_csv(in_file, header=1, dtype='str')
    all_stock = np.array(all_stock)
    all_id = all_stock[:,0]
    stk_id = ''
    base_idx = 0
    stk_info = []
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
    return all_stock, stk_info, base_info

def getSimilarK(in_file, base_id, comp_len):
    all_stock, stk_info, base_info = readDailyK(in_file, base_id)
    
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
    return all_stock, stk_sort

def get_mink(stk, k_len):
    o = stk[:,2][:k_len]
    o = o.astype(np.float)
    h = stk[:,3][:k_len]
    h = h.astype(np.float)
    l = stk[:,4][:k_len]
    l = l.astype(np.float)
    c = stk[:,5][:k_len]
    c = c.astype(np.float)
    return [o, h, l, c]

def showFutChart(txff, txff_sort, k_len=300):
    idx = 0
    for info in txff_sort:
        idx += 1
        if idx > 10:
            break
        start = int(info[1])
        end = int(info[2]) + 1
        fut = txff[start:end]
        close = fut[:,5]
        pad_len = k_len - len(close)
        close = close.astype(np.float)
        pad_close = float(close[-1])
        close = np.pad(close, (0, pad_len), 'constant', constant_values=(0,pad_close))
        name = info[0] + ':  ' + str(round(float(info[3]) * 100, 2)) + '%'
        df = pd.DataFrame(close, columns=[name])
        df.plot()

def readMin1K(in_file):
    txff = pd.read_csv(in_file, header=1, dtype='str')
    txff = np.array(txff)
    txff_date = txff[:,0]
    date = ''
    txff_info = []
    info = []
    for i in range(len(txff_date)):
        if date != txff_date[i]:
            if len(info) > 0:
                txff_info.append(info)
            date = txff_date[i]
            info = [date, i, i, 0.0]
        else:
            info[2] = i
            
    if len(info) > 0:
        txff_info.append(info)
    return txff, txff_info

def getSimilarMin1K(in_file, comp_len=300):
    txff, txff_info = readMin1K(in_file)
    
    base_info = txff_info[-1]
    start = base_info[1]
    end = base_info[2] + 1
    txff_base = txff[start:end]
    k_base = get_mink(txff_base, comp_len)
    
    for info in txff_info:
        start = info[1]
        end = info[2] + 1
        fut = txff[start:end]
        k = get_mink(fut, comp_len)
        if len(k[0]) == comp_len:
            info[3] = get_corrc(k_base, k)
    
    txff_sort = np.array(txff_info)
    sort = txff_sort[:,3]
    sort = sort.astype(np.float)
    txff_sort = txff_sort[np.argsort(sort)][::-1]
    return txff, txff_sort


mydir = 'D:\\MITAKE\\VSProject\\MitakeSmartV2\\Project\\deploy\\'
#mydir = '/home/jashingden/GitHub/'
in_file = mydir + 'DailyK_20210104.csv'
out_file = mydir + 'SimilarK.csv'
min_file = mydir + 'TXFF_Min1K_Data.csv'

base_id = '6488'
k_len = 1000
comp_len = 100
#all_stock, stk_sort = getSimilarK(in_file, base_id, comp_len)
#saveCSV(out_file, stk_sort)
#showChart(all_stock, stk_sort, comp_len)

txff, txff_sort = getSimilarMin1K(min_file, 100)
#saveCSV(out_file, txff_sort)
showFutChart(txff, txff_sort)
