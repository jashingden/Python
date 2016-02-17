#-*-coding:UTF-8 -*-
#  EX07_07.py
#  
#  file 寫檔範例 write()
#  亂數產生10個整數(1~1000)，寫入檔案中

import random
file = open('rand_num.txt', 'w', encoding = 'UTF-8')
for i in range(10):
    file.write( str(random.randint(1,1000))+'\n' )
file.close()
