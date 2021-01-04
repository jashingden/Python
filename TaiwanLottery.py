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
factorList = [factor1, factor2, factor3]
factorDesc = ['01-07 08-13 14-19 20-25 26-31 32-38', '01-06 07-12 13-18 19-24 25-30 31-38', '01-05 06-10 11-15 16-22 23-29 30-38']

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
        formdata['SuperLotto638Control_history1$dropYear'] = year
        formdata['SuperLotto638Control_history1$dropMonth'] = month
        page = browser.post(start_url, data=formdata)
    span_list = page.soup.find_all("span")
    lotto_tag = "SuperLotto638Control_history1_dlQuery_"
    lotto_list = []
    lotto = []
    for span in span_list:
        if len(lotto) >= 9:
            lotto_list.append(lotto)
            lotto = []
        if not (span.get("id") is None):
            sid = span["id"]
            if lotto_tag+'DrawTerm' in sid or lotto_tag+'Date' in sid or lotto_tag+'No' in sid:
                lotto.append(span.text)
    if len(lotto) >= 9:
        lotto_list.append(lotto)
    return lotto_list

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
    
def getZoneKey(zone):
    key = str(zone[0])+str(zone[1])+str(zone[2])+str(zone[3])+str(zone[4])+str(zone[5])#+str(zone[6])
    return key

def getZoneCount(zoneKey):
    count = []
    for zone in zoneKey:
        count.append(int(zone))
    return count
    
'''
依分區統計開獎號碼分佈
'''
def calcRate_m1(mylist, factor, basic = 10, dump = False):
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
def calcRate_m2(mylist, factor, basic = 2):
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
    key = row[2]+'_'+row[3]+'_'+row[4]+'_'+row[5]+'_'+row[6]+'_'+row[7]
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
    for i in range(2, 8):
        l = lotto[i]
        for j in range(2, 8):
            r = row[j]
            if r == l:
                zone += 1
                break
    if lotto[8] == row[8]:
        if zone == 6:
            msg = '恭喜中頭獎'
        elif zone == 5:
            msg = '恭喜中參獎15萬元'
            prize = 150000
        elif zone == 4:
            msg = '恭喜中伍獎4千元'
            prize = 4000
        elif zone == 3:
            msg = '恭喜中柒獎4百元'
            prize = 400
        elif zone == 2:
            msg = '恭喜中捌獎2百元'
            prize = 200
        elif zone == 1:
            msg = '恭喜中普獎1百元'
            prize = 100
    else:
        if zone == 6:
            msg = '恭喜中貳獎'
        elif zone == 5:
            msg = '恭喜中肆獎2萬元'
            prize = 20000
        elif zone == 4:
            msg = '恭喜中陸獎8百元'
            prize = 800
        elif zone == 3:
            msg = '恭喜中玖獎1百元'
            prize = 100
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
    total = 100 * len(mylist)
    print('總花費', total, '中獎金額', prize)

def showFactorRate(lottolist):
    print('sample count', len(lottolist))
    for i in range(0, len(factorList)):
        print('factor', factorDesc[i])
        factor = factorList[i]
        calcRate_m1(lottolist, factor, 10)
        calcRate_m2(lottolist, factor)
        print('--------------------')
    calcRepeat(lottolist)

def pickMy(lottolist, factor, basic = 10):
    mylist = []
    rateItem = calcRate_m1(lottolist, factor, basic)
    f = [1]
    f.extend(factor)
    f.append(39)
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
        mylotto.append(random.randint(1, 8))
        print(item, mylotto)
        my = [lottolist[0][0], lottolist[0][1]]
        my.extend(mylotto)
        mylist.append(my)
    return mylist


#更新各期獎號
newlist = updateLotto('TaiwanLottery.csv')

lottolist = loadCSV(mydir + 'TaiwanLottery.csv', False)
showFactorRate(lottolist)

# [6,11,16,23,30] '01-05 06-10 11-15 16-22 23-29 30-38'
myfactor = factor1
#mylist = pickMy(lottolist, myfactor, 10)

mylist = loadCSV(mydir + 'TaiwanLotteryMy.csv', False)
#calcHistory(lottolist, mylist)
for lotto in newlist:
    calcMy(lotto, lottolist, mylist, myfactor)

