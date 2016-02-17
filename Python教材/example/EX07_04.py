#-*-coding:UTF-8 -*-
#  EX07_04.py
#  
#  file 讀檔範例 read()
#  

file = open('dream.txt', 'r', encoding='UTF-8')
content = file.read()
print(content)
file.close()