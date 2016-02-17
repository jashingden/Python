#-*-coding:UTF-8 -*-
#  EX04_06.py
#
#  全域變數範例
#  

#name 變數宣告在最外層，為全域變數
name = "Tony"

def change_name(n):
    global name    
    name = n
    print('In change_name function, name=%s' % name)

print('Before change_name function called, name=%s' % name)
change_name('John')
print('After change_name function called, name=%s' % name)
