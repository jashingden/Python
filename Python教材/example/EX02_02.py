#-*-coding:UTF-8 -*-
#範例程式 EX02_02.py
#判斷輸入的數字是奇數還是偶數

num = int(input('Please input a num:'))

if num % 2 == 0:
    print(num,'是偶數')
else:
    print(num,'是奇數')