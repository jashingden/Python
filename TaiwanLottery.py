# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 17:22:01 2018

@author: eddyteng
"""
import os
import csv
import urllib.request
from bs4 import BeautifulSoup
import mechanicalsoup

"""
第1個選號區中的01 ~ 38的號碼中任選6個號碼，
第2個選號區中的01 ~ 08的號碼中任選1個號碼，
"""
home = "http://www.taiwanlottery.com.tw/lotto/"
name = "威力彩"
url = "superlotto638/history.aspx"
"""
01-07 08-13 14-19 20-25 26-31 32-38
01-06 07-12 13-18 19-24 25-30 31-38
01-05 06-10 11-15 16-22 23-29 30-38
"""
factor1 = [8,14,20,26,32]
factor2 = [7,13,19,25,31]
factor3 = [6,11,16,23,30]

def parse_url(url, year, month):
    start_url = home + url
    '''
    #設置假的瀏覽器資訊
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
    req = urllib.request.Request(url=start_url,headers=headers)
    page = urllib.request.urlopen(req)
    contentBytes = page.read()
    soup = BeautifulSoup(str(contentBytes), "html.parser")
    '''
    browser = mechanicalsoup.StatefulBrowser()
    page = browser.get(start_url)
    form = page.soup.find('form')
    fields = form.findAll('input')
    formdata = dict( (field.get('name'), field.get('value')) for field in fields )
    formdata['SuperLotto638Control_history1$dropYear'] = year
    formdata['SuperLotto638Control_history1$dropMonth'] = month
    page = browser.post(start_url, data=formdata)
    span_list = page.soup.find_all("span")
    lotto = "SuperLotto638Control_history1_dlQuery_"
    lotto_list = []
    for span in span_list:
        if not (span.get("id") is None):
            sid = span["id"]
            if lotto+'DrawTerm' in sid or lotto+'Date' in sid or lotto+'No' in sid:
                lotto_list.append(span.text)
    for x in range(0, len(lotto_list), 9):
        print('%s,%s,%s,%s,%s,%s,%s,%s,%s' % (lotto_list[x], lotto_list[x+1], lotto_list[x+2], lotto_list[x+3], lotto_list[x+4], lotto_list[x+5], lotto_list[x+6], lotto_list[x+7], lotto_list[x+8]))

#parse_url(url, 107, 12)

def loadCSV(path, dump=True):
    file = open(path, 'r')
    mylist = []
    for row in csv.reader(file):
        mylist.append(row)
        if dump:
            print(row)
    return mylist

def calcZone(row, factor):
    zone = [0,0,0,0,0,0,0]
    numbers = [int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7])]
    for num in numbers:
        if num < factor[0]:
            zone[0] = zone[0]+1
        elif num < factor[1]:
            zone[1] = zone[1]+1
        elif num < factor[2]:
            zone[2] = zone[2]+1
        elif num < factor[3]:
            zone[3] = zone[3]+1
        elif num < factor[4]:
            zone[4] = zone[4]+1
        else:
            zone[5] = zone[5]+1
    zone[6]=int(row[8])
    return zone
    
'''
依分區統計開獎號碼分佈
'''
def calcRate_m1(mylist, factor, basic = 10, dump=True):
    rate = {}
    for row in mylist:
        zone = calcZone(row, factor)
        key = str(zone[0])+str(zone[1])+str(zone[2])+str(zone[3])+str(zone[4])+str(zone[5])#+str(zone[6])
        count = rate.get(key, 0)
        rate[key] = count+1
    i = 0
    count = len(mylist)
    for item, value in rate.items():
        if value >= basic:
            i += 1
            print(i, item, value, '%.2f%%' % (value/count*100))
            if dump:
                for row in mylist:
                    zone = calcZone(row, factor)
                    key = str(zone[0])+str(zone[1])+str(zone[2])+str(zone[3])+str(zone[4])+str(zone[5])#+str(zone[6])
                    if key == item:
                        print(row)
    print('total', len(rate))

'''
連續兩組開獎號碼分佈
'''
def calcRate_m2(mylist, factor, basic = 2):
    rate = {}
    key2 = None
    for row in mylist:
        zone = calcZone(row, factor)
        key = str(zone[0])+str(zone[1])+str(zone[2])+str(zone[3])+str(zone[4])+str(zone[5])#+str(zone[6])
        if key2 is None:
            key2 = key
            continue
        key3 = key2 + '_' + key
        count = rate.get(key3, 0)
        rate[key3] = count+1
        key2 = key
    if len(mylist) == len(rate):
        print('no continous')
    else:
        i = 0
        for item, value in rate.items():
            if value >= basic:
                i += 1
                print(i, item, value)

'''
檢查是否有重複的開獎號碼
'''
def calcRepeat(mylist):
    repeat = {}
    for row in mylist:
        key = row[2]+'_'+row[3]+'_'+row[4]+'_'+row[5]+'_'+row[6]+'_'+row[7]
        count = repeat.get(key, 0)
        repeat[key] = count+1
    if len(mylist) == len(repeat):
        print('no repeat')
    else:
        i = 0
        for item, value in repeat.items():
            if value > 1:
                i += 1
                print(i, item, value)

def calcPrize(lotto, row):
    prize = 0
    zone = 0
    for i in range(2, 8):
        l = lotto[i]
        for j in range(2, 8):
            r = row[j]
            if r == l:
                zone += 1
                break
    if lotto[8] == row[8]:
        if zone == 6:
            print('恭喜中頭獎')
        elif zone == 5:
            print('恭喜中參獎15萬元')
            prize = 150000
        elif zone == 4:
            print('恭喜中伍獎4千元')
            prize = 4000
        elif zone == 3:
            print('恭喜中柒獎4百元')
            prize = 400
        elif zone == 2:
            print('恭喜中捌獎2百元')
            prize = 200
        elif zone == 1:
            print('恭喜中普獎1百元')
            prize = 100
    else:
        if zone == 6:
            print('恭喜中貳獎')
        elif zone == 5:
            print('恭喜中肆獎2萬元')
            prize = 20000
        elif zone == 4:
            print('恭喜中陸獎8百元')
            prize = 800
        elif zone == 3:
            print('恭喜中玖獎1百元')        
            prize = 100
    return prize

def calcMy(lottolist, mylist, factor):
    repeat = {}
    for row in lottolist:
        key = row[2]+'_'+row[3]+'_'+row[4]+'_'+row[5]+'_'+row[6]+'_'+row[7]
        repeat[key] = 1
    prize = 0
    for row in mylist:
        key = row[2]+'_'+row[3]+'_'+row[4]+'_'+row[5]+'_'+row[6]+'_'+row[7]
        if repeat.get(key, 0) > 0:
            isRepeat = "repeat"
        else:
            isRepeat = "no repeat"
        zone = calcZone(row, factor)
        key = str(zone[0])+str(zone[1])+str(zone[2])+str(zone[3])+str(zone[4])+str(zone[5])#+str(zone[6])
        print(key, row, isRepeat)
        prize += calcPrize(lottolist[0], row)
    total = 100 * len(mylist)
    print('總花費', total, '中獎金額', prize)

# ['107000095', '107/11/26', '01', '16', '25', '30', '31', '32', '07']
lottolist = loadCSV('D:\EddyTeng\Git\Python\TaiwanLottery.csv', False)
mylist = loadCSV('D:\EddyTeng\Git\Python\TaiwanLotteryMy.csv', False)
myfactor = factor3
print('sample count', len(lottolist))
factorList = [factor1, factor2, factor3]
factorDesc = ['01-07 08-13 14-19 20-25 26-31 32-38', '01-06 07-12 13-18 19-24 25-30 31-38', '01-05 06-10 11-15 16-22 23-29 30-38']
for i in range(0, len(factorList)):
    print('factor', factorDesc[i])
    factor = factorList[i]
    calcRate_m1(lottolist, factor, 9, False)
    calcRate_m2(lottolist, factor)
    print('--------------------')
calcRepeat(lottolist)
calcMy(lottolist, mylist, myfactor)
