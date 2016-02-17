#-*-coding:UTF-8 -*-
#  EX04_01.py
#  改寫 EX02_05.py 的程式，將其寫成函式版本
# 

def summation(n):
    total = 0
    for i in range(1,n+1):
        # total += i  等價於 total = total + i
        total += i
    print('Total is:',total)

#函式宣告完之後才能呼叫
summation(100)
