#-*-coding:UTF-8 -*-
# 範例程式 EX02_06.py
#
# 輸入一個數字n，計算1+2+3+...+n的總和為多少?
# (while 迴圈版本)

n = int(input('Please input n:'))
total = 0
i = 1

while i <= n:
    # total += i  等價於 total = total + i
    total += i
    i += 1
print('Total is:',total)