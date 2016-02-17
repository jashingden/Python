#-*-coding:UTF-8 -*-
#  EX04_04.py
#
#  不定個數參數 ** (dict)
#  傳入多個成員資訊 姓名=年齡(數量可以動態增減)當引數
#  對每個成員打招呼

def hello(**names):
    for n in names:
        print("Hello %s, you're %d years old"%(n,names[n]))

hello(John=25, Tom=20, Bob=33, Tony=18)
