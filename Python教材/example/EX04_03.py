#-*-coding:UTF-8 -*-
#  EX04_03.py
#
#  不定個數參數 * (tuple)
#  傳入多個成員資訊 姓名(數量可以動態增減)當引數
#  對每個成員打招呼

def hello(*names):
    for n in names: print("Hello, %s."%n)

hello("Tom","Peter","Bob","Rain")
