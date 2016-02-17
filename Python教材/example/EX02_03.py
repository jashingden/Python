#-*-coding:UTF-8 -*-
#範例程式 EX02_03.py
#輸入兩個數字比大小

num1 = int(input('Please input a num1:'))
num2 = int(input('Please input a num2:'))

if num1 == num2:
    print(num1,'等於',num2)
elif num1 < num2:
    print(num1,'小於',num2)
else:
    print(num1,'大於',num2)