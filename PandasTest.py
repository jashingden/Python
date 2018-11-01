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

df = pd.read_csv('D:\MITAKE\VSProject\MitakePortfolio\GPHONE_MTK.csv',
        sep='\t', names=['PID', 'Org', 'UserID', 'Stocks', 'SN', 'HID', 'UpdateDT'])

df.head()

df['Stocks'].iloc[3].split('@')[2]