# encoding: utf-8
import getpass
from redmine import Redmine

#Redmine帳號
username = 'eddyteng'
#Redmine密碼
password = getpass.getpass('Please input your password: ')
#Redmine專案項目的ID
issue_id = 14962

var = raw_input('Text encoding is UTF-8 ? (y/n) ')
if var in ('y', 'Y'):
        text_utf8 = True
else:
        text_utf8 = False

redmine = Redmine('https://redmine.mitake.com.tw/redmine', username=username, password=password)
my = redmine.issue.get(issue_id)

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

title = 'ID,標題,開始日期,完成日期,完成百分比,預估工時,耗用工時'
if text_utf8:
	print title
else:
	print title.decode('utf8').encode('big5')

showIssueValue(my)
