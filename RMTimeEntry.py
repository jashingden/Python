# encoding: utf-8
import getpass
import csv
from redmine import Redmine
from datetime import datetime

#關閉警告訊息
import warnings
warnings.filterwarnings('ignore')

#Redmine帳號/密碼
username = 'eddyteng'
password = getpass.getpass('Please input your password: ')
redmine = Redmine('https://redmine.mitake.com.tw/redmine', username=username, password=password, requests={'verify': False})

def addTimeEntry(issue, date, work, hours=8, work_overtime=False):
        if work_overtime:
                return redmine.time_entry.create(issue_id=issue, spent_on=date, hours=hours, comments=work, activity_id=11, custom_fields=[{'id': '3', 'value': '1'}])
        else:
                return redmine.time_entry.create(issue_id=issue, spent_on=date, hours=hours, comments=work, activity_id=11)

def addTimeEntries(mylist):
        for row in mylist:
                datestr = row[0].split("/")
                date = "{0}-{1}-{2}".format(datestr[0], datestr[1].zfill(2), datestr[2].zfill(2))
                if float(row[3]) > 8:
                    addTimeEntry(row[5], date, row[2])
                    addTimeEntry(row[5], date, row[2], float(row[3])-8, True)
                else:
                    addTimeEntry(row[5], date, row[2], row[3])

def loadCSV(path, dump=True):
        file = open(path, 'r')
        mylist = []
        for row in csv.reader(file):
                mylist.append(row)
                if dump:
                        print(row)
        return mylist

# 範例
# entry = addTimeEntry(12959, '2016-01-04', u'GitLab版控轉換測試', 5.5)
# entry = addTimeEntry(7001, '2016-01-13', u'數據中心電文介接', 1, True)

# ['2017/2/9', '行動股市', 'Android自動化測試使用Espresso', '8', '', '39872']
# 範例
# mylist = loadCSV('D:\EddyTeng\Git\Python\RMTimeEntry.csv')
# addTimeEntries(mylist)
