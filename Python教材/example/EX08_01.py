#-*-coding:UTF-8 -*-
#  EX08_01.py
#  
#  pyqrcode 使用範例
#  
from pyqrcode import QRCode
url = QRCode('http://www.ntu.edu.tw')
#輸出SVG格式檔案:url.svg ,縮放比為10
url.svg('url.svg', scale=10)
#輸出PNG格式檔案:url.png ,縮放比為10
url.png('url.png', scale=10)
