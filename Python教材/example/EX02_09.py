#-*-coding:UTF-8 -*-
# 範例程式 EX02_09.py
#
# break 範例
# 電腦以亂數產生一數介於1~100之間(num)之後，使用者不斷猜測該數(guess)，
# 每次猜測時電腦必須提示猜的太大或太小，此動作一直重複直到猜中為止。
#
import random
num = random.randint(1,100)
count = 1
while True:
    print("第",count,"次猜測")
    guess = int(input('Please input num:'))
    if guess == num:
        print("恭喜答對!! 數字的確是 ",num)
        break
    elif guess < num:
        print("猜錯囉，你猜的太小了")
    else:
        print("猜錯囉，你猜的太大了")
    count+=1