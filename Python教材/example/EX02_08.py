#-*-coding:UTF-8 -*-
# 範例程式 EX02_08.py
#
# continue 範例
# 將 2到100中的偶數相加，但必須排除10的倍數，也就是2+4+6+8+12+14+.....，最後印出總和。
#

sum = 0
for i in range(2,101,2):
    if i % 10 == 0:
        continue
    sum += i
print("總和:",sum)
