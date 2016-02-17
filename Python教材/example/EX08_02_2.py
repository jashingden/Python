#-*-coding:UTF-8 -*-
#  EX08_02_2.py
#  
#  模組範例檔_2
#  
import EX08_02_1

if __name__ == '__main__':
    print('模組範例檔_2')

tools = EX08_02_1.tools()
print(tools.generate_random_nums(10))