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
import random
from mysys import *

"""
第1個選號區中的01 ~ 38的號碼中任選6個號碼，
第2個選號區中的01 ~ 08的號碼中任選1個號碼，
"""
home = "https://www.taiwanlottery.com.tw/lotto/"
name = "今彩539"
url = "DailyCash/history.aspx"
"""
01-08 09-16 17-24 25-32 33-39
01-10 11-16 17-26 27-32 33-39
01-09 10-17 18-25 25-33 34-39
"""
factor1 = [9,17,25,33]
factor2 = [11,17,27,33]
factor3 = [10,18,25,34]
factorList = [factor1, factor2, factor3]
factorDesc = ['01-08 09-16 17-24 25-32 33-39', '01-10 11-16 17-26 27-32 33-39', '01-09 10-17 18-25 25-33 34-39']

def parse_url(url, year=0, month=0):
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
    if year > 0 and month > 0:
        form = page.soup.find('form')
        fields = form.findAll('input')
        formdata = dict( (field.get('name'), field.get('value')) for field in fields )
        formdata['D539Control_history1$dropYear'] = year
        formdata['D539Control_history1$dropMonth'] = month
        page = browser.post(start_url, data=formdata)
    span_list = page.soup.find_all("span")
    lotto_tag = "D539Control_history1_dlQuery_"
    lotto_list = []
    lotto = []
    for span in span_list:
        if len(lotto) >= 7:
            lotto_list.append(lotto)
            lotto = []
        if not (span.get("id") is None):
            sid = span["id"]
            if lotto_tag+'D539_DrawTerm' in sid or lotto_tag+'D539_DDate' in sid or lotto_tag+'No' in sid:
                lotto.append(span.text)
    if len(lotto) >= 7:
        lotto_list.append(lotto)
    return lotto_list

'''
def updateLottoAll(csv):
    lottolist = []
    for i in range(103, 110):
        for m in range(1, 13):
            if i == 109 and m > 3:
                break
            newlist = []
            newlottolist = parse_url(url, i, m)
            for lotto in newlottolist:
                newlist.append(lotto)
            lottolist = newlist + lottolist
    if len(lottolist) > 0:
        file = mydir + csv
        saveCSV(file, lottolist)
'''

def updateLotto(csv, dump=True):
    #parse_url(url, 107, 12)
    newlottolist = parse_url(url)
    file = mydir + csv
    lottolist = loadCSV(file, False)
    curr = lottolist[0][0]
    newlist = []
    for lotto in newlottolist:
        if lotto[0] > curr:
            newlist.append(lotto)
        else:
            break;
    if len(newlist) > 0:
        if dump:
            print('有新的開獎號碼:', newlist)
        lottolist = newlist + lottolist
        saveCSV(file, lottolist)
    return newlist

# ['107000095', '107/11/26', '01', '16', '25', '30', '31', '32', '07']
def loadCSV(path, dump=True):
    file = open(path, 'r')
    mylist = []
    for row in csv.reader(file):
        mylist.append(row)
        if dump:
            print(row)
    return mylist

def saveCSV(path, mylist):
    file = open(path, 'w', newline='')
    writer = csv.writer(file)
    writer.writerows(mylist)

def calcZone(row, factor):
    zone = [0,0,0,0,0,0]
    numbers = [int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6])]
    for num in numbers:
        if num < factor[0]:
            zone[0] = zone[0]+1
        elif num < factor[1]:
            zone[1] = zone[1]+1
        elif num < factor[2]:
            zone[2] = zone[2]+1
        elif num < factor[3]:
            zone[3] = zone[3]+1
        else:
            zone[4] = zone[4]+1
    return zone
    
def getZoneKey(zone):
    key = str(zone[0])+str(zone[1])+str(zone[2])+str(zone[3])+str(zone[4])
    return key

def getZoneCount(zoneKey):
    count = []
    for zone in zoneKey:
        count.append(int(zone))
    return count
    
'''
依分區統計開獎號碼分佈
'''
def calcRate_m1(mylist, factor, basic = 50, dump = False):
    rate = {}
    rateItem = []
    for row in mylist:
        zone = calcZone(row, factor)
        key = getZoneKey(zone)
        count = rate.get(key, 0)
        rate[key] = count+1
    i = 0
    count = len(mylist)
    top = 0
    for item, value in rate.items():
        if value >= basic:
            rateItem.append(item)
            i += 1
            top += value
            print(i, item, value, '%.2f%%' % (value/count*100))
            if dump:
                for row in mylist:
                    zone = calcZone(row, factor)
                    key = getZoneKey(zone)
                    if key == item:
                        print(row)
            else:
                zone = calcZone(mylist[0], factor)
                key = getZoneKey(zone)
                if key == item:
                    print(mylist[0])
                
    print('total', len(rate), 'top', top)
    return rateItem

'''
連續兩組開獎號碼分佈
'''
def calcRate_m2(mylist, factor, basic = 5):
    rate = {}
    key2 = None
    for row in mylist:
        zone = calcZone(row, factor)
        key = getZoneKey(zone)
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

def getRepeatKey(row):
    key = row[2]+'_'+row[3]+'_'+row[4]+'_'+row[5]+'_'+row[6]
    return key
    
'''
檢查是否有重複的開獎號碼
'''
def calcRepeat(mylist):
    repeat = {}
    for row in mylist:
        key = getRepeatKey(row)
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

def calcPrize(lotto, row, dump = True):
    prize = 0
    zone = 0
    msg = '';
    for i in range(2, 7):
        l = lotto[i]
        for j in range(2, 7):
            r = row[j]
            if r == l:
                zone += 1
                break
    if zone == 5:
        msg = '恭喜中頭獎800萬元'
        prize = 8000000
    elif zone == 4:
        msg = '恭喜中貳獎2萬元'
        prize = 20000
    elif zone == 3:
        msg = '恭喜中參獎3百元'
        prize = 300
    elif zone == 2:
        msg = '恭喜中肆獎50元'
        prize = 50
    if dump and (prize > 0 or len(msg) > 0):
        print(msg)
    return prize

def calcHistory(lottolist, mylist, basic = 1000):
    total = 0
    for lotto in lottolist:
        for row in mylist:
            prize = calcPrize(lotto, row, False)
            total += prize
            if (prize >= basic):
                print('中獎金額', prize, lotto)
    cost = 100 * len(mylist) * len(lottolist)
    print('總花費', cost, '總中獎金額', total)
    return total
    
def calcMy(lotto, lottolist, mylist, factor):
    print('最新開獎號碼', lotto)
    repeat = {}
    for row in lottolist:
        key = getRepeatKey(row)
        repeat[key] = 1
    prize = 0
    for row in mylist:
        key = getRepeatKey(row)
        if repeat.get(key, 0) > 0:
            isRepeat = "repeat"
        else:
            isRepeat = "no repeat"
        zone = calcZone(row, factor)
        key = getZoneKey(zone)
        print(key, row, isRepeat)
        prize += calcPrize(lotto, row)
    total = 50 * len(mylist)
    print('總花費', total, '中獎金額', prize)

def showFactorRate(lottolist):
    print('sample count', len(lottolist))
    for i in range(0, len(factorList)):
        print('factor', factorDesc[i])
        factor = factorList[i]
        calcRate_m1(lottolist, factor, 50)
        calcRate_m2(lottolist, factor)
        print('--------------------')
    calcRepeat(lottolist)

def pickMy(lottolist, factor, basic = 50):
    mylist = []
    rateItem = calcRate_m1(lottolist, factor, basic)
    f = [1]
    f.extend(factor)
    f.append(40)
    for item in rateItem:
        mylotto = []
        count = getZoneCount(item)
        i = 0
        for c in count:
            while c > 0:
                num = random.randint(f[i],f[i+1]-1)
                if num not in mylotto:
                    mylotto.append(num)
                    c -= 1
            i += 1
        print(item, mylotto)
        my = [lottolist[0][0], lottolist[0][1]]
        my.extend(mylotto)
        mylist.append(my)
    return mylist


#更新各期獎號
newlist = updateLotto('TaiwanLottery539.csv')

lottolist = loadCSV(mydir + 'TaiwanLottery539.csv', False)
showFactorRate(lottolist)

myfactor = factor1
#mylist = pickMy(lottolist, myfactor, 50)

mylist = loadCSV(mydir + 'TaiwanLotteryMy539.csv', False)
#calcHistory(lottolist, mylist)
for lotto in newlist:
    calcMy(lotto, lottolist, mylist, myfactor)

