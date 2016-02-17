# encoding: utf-8
import getpass
from redmine import Redmine

#輸出文字是否UTF-8編碼
text_utf8 = True

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
# 一般工時
# entry = addTimeEntry(12959, '2016-01-04', u'GitLab版控轉換測試', 5.5)
# 加班工時
# entry = addTimeEntry(7001, '2016-01-13', u'數據中心電文介接', 1, True)

def showIssueValue(my):
	value = "%d,%s,%s,%s,%s%%,%s,%s" % (my.id, my.subject, my.start_date, my.due_date, my.done_ratio, my.estimated_hours, my.spent_hours)
	if text_utf8:
		print value.encode('utf8')
	else:
		print value.encode('big5')
		
	if my.children is not None:
		for iss in my.children:
			sub = redmine.issue.get(iss.id)
			showIssueValue(sub)

# 範例
# issue_id = 14962
# my = redmine.issue.get(issue_id)
# showIssueValue(my)

def dump(obj):
        for attr in dir(obj):
                print "%s = %s" % (attr, getattr(obj, attr))

def dumpTimeEntry(time_entries):
        for entry in time_entries:
                print "%s %s(#%d) %d hr %s" % (entry.spent_on, entry.project.name, entry.issue.id, entry.hours, entry.comments)

# 範例
# user = redmine.user.get(376)
# dump(user)
# dumpTimeEntry(user.time_entries)    
