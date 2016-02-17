#-*-coding:UTF-8 -*-
#  EX07_06.py
#  
#  file 讀檔範例 readlines()
#  

file = open('dream.txt', 'r', encoding='UTF-8') 
for line in file.readlines():
    print(line, end='')
file.close()