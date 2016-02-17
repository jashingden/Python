#-*-coding:UTF-8 -*-
# 類別作業練習 EX05_hw.py
#
# 測試資料 http://140.112.31.82/wordpress/?p=216

class student:

    def __init__(self, n, g):
        self.name = n
        self.gender = g
        self.grades = []

    def add(self,grade):
        #do something.

    def avg(self):
        #do something.
        #return avg_grade

    def fcount(self):
        #do something.
        #return fail_count

s1 = student("Tom","M")
s2 = student("Jane","F")
s3 = student("John","M")
s4 = student("Ann","F")
s5 = student("Peter","M")
s1.add(80)
s1.add(90)
s1.add(55)
s1.add(77)
s1.add(40)
s2.add(58)
s2.add(87)
s3.add(100)
s3.add(80)
s4.add(40)
s4.add(55)
s5.add(60)
s5.add(60)