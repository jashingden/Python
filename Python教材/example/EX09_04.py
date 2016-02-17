#-*-coding:UTF-8 -*-
#  EX09_04.py
#  
#  捷運站查詢範例
#  
import urllib.request
import urllib.parse
from html.parser import HTMLParser

data = urllib.parse.urlencode({'s1elect': '012', 'action':'query','s2elect':'071','submit':'確定'})
data = data.encode('utf-8')
response = urllib.request.urlopen("http://web.trtc.com.tw/c/2stainfo_new.asp", data)
html = response.read().decode('utf_8')

class myparser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.isNumber = 0
        self.numbers = []
    def handle_data(self, data):
        if self.isNumber == 1:
            print(data)
    def handle_starttag(self, tag, attrs):
        if tag == 'font' and attrs == [('size','-1')]:
            self.isNumber = 1
    def handle_endtag(self, tag):
        if tag == 'font' and self.isNumber == 1:
            self.isNumber = 0

Parser = myparser()
Parser.feed(html)
