#-*-coding:UTF-8 -*-
#  EX07_05.py
#  
#  file 讀檔範例 readline()
#  

file = open('dream.txt', 'r', encoding='UTF-8')
while True:
    line = file.readline() 
    if not line: 
        break 
    print(line, end='')
file.close()
