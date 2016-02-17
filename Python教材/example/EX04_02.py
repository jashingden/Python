#-*-coding:UTF-8 -*-
#  EX04_02.py
#
#  函數的預設值為可變物件

print('========append_item=========')

def append_item(item, lis=[]):
    lis.append(item)
    return lis

print(append_item('apple'))
print(append_item('orange'))
print(append_item('peach'))

#============================
print('========append_item_v2=========')

def append_item_v2(item,lis=[]):
    lis.append(item)
    return lis
lis = []
print(append_item_v2('apple',lis))
print(append_item_v2('banana'))
print(append_item_v2('watermelon'))
print(append_item_v2('orange',lis))
print(append_item_v2('peach',lis))

#============================
print('========append_item_v3=========')

def append_item_v3(item):
    lis=[]
    lis.append(item)
    return lis

print(append_item_v3('apple'))
print(append_item_v3('orange'))
print(append_item_v3('peach'))

