#-*-coding:UTF-8 -*-
#  EX09_01.py
#  
#  使用 urllib 讀取網頁內容範例
#  

import urllib.request
response = urllib.request.urlopen('http://invoice.etax.nat.gov.tw/')
html = response.read().decode('utf_8')
print(html)
