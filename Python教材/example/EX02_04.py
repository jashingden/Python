#-*-coding:UTF-8 -*-
# 範例程式 EX02_04.py
#
# 計算BMI並輸出分級值
#
# BMI = 體重 (kg) / 身高 (m^2)
'''
成人的體重分級與標準
分   級    身體質量指數
體重過輕    BMI ＜ 18.5
正常範圍    18.5 ≦ BMI ＜24
過   重    24 ≦ BMI ＜ 27
輕度肥胖    27 ≦ BMI ＜ 30
中度肥胖    30 ≦ BMI ＜ 35
重度肥胖    BMI ≧ 35
'''

height = int(input('Please input a height(cm):'))
weight = int(input('Please input a weight(kg):'))

BMI = weight / float(height/100)**2

print("BMI:",BMI)

if BMI < 18.5:
    print('體重過輕')
elif 18.5 <= BMI < 24:
    print('正常範圍')
elif 24 <= BMI < 27:
    print('過   重')
elif 27 <= BMI < 30:
    print('輕度肥胖')
elif 27 <= BMI < 30:
    print('輕度肥胖')
elif 30 <= BMI < 35:
    print('中度肥胖')
else:
    print('重度肥胖')