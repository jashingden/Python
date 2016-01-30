# encoding: utf-8
import getpass
from redmine import Redmine

#Redmine帳號/密碼
username = 'eddyteng'
password = getpass.getpass('Please input your password: ')
redmine = Redmine('https://redmine.mitake.com.tw/redmine', username=username, password=password)

def addTimeEntry(issue, date, work, hours=8, work_overtime=False):
        if work_overtime:
                return redmine.time_entry.create(issue_id=issue, spent_on=date, hours=hours, comments=work, activity_id=11, custom_fields=[{'id': '3', 'value': '1'}])
        else:
                return redmine.time_entry.create(issue_id=issue, spent_on=date, hours=hours, comments=work, activity_id=11)

# 範例
# entry = addTimeEntry(12959, '2016-01-04', u'GitLab版控轉換測試', 5.5)
# entry = addTimeEntry(7001, '2016-01-13', u'數據中心電文介接', 1, True)
