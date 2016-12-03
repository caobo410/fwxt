# -*- coding: utf-8 -*-
import random
# a = raw_input('请输入客户数字：')
# b = raw_input('请输入固定位数：')
# c = raw_input('请输入数量：')
kh = 123
gd = 16
num = 100000
str_bs = '000000000000000000'
str_num = '100000000000000000000'
ws = gd/2 - 1
min_str = str_num[:ws]
max_str = str_num[:ws+1]
min_num = int(min_str) + num
max_num = int(max_str) - 1
all_the_text=''
for i in range(1, num):
    one = random.randint(10, 99)
    str_one = str(one)
    int_one = one // 10
    int_two = one % 10
    sj = random.randint(min_num, max_num)
    str1 = str(sj)
    code = (str_bs+str(i))
    cd = 0-(ws - len(str(kh)))
    str2 = str(kh)+code[cd:]
    str3 = ''
    for j in range(0, gd/2-1):
        if int(str_one[:1]) % 2 == 0:
            str3 = str3 + str1[j] + str2[j]
        else:
            str3 = str3 + str2[j] + str1[j]
    int_end = int_two - gd + 2
    str3 = str3[int_end:] + str3[:int_two]
    str4 = str_one + str3
    num = num + 1
    all_the_text = all_the_text + str4 +'\n'
    if num == 100:
        file_object = open('d://557.txt', 'a')
        file_object.write(all_the_text)
        file_object.close()
        all_the_text = ''
        num = 0
if num > 0:
    file_object = open('d://557.txt', 'a')
    file_object.write(all_the_text)
    file_object.close()