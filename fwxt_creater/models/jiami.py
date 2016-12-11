# -*- coding: utf-8 -*-
import random
kh = '323'
gd = 16
num = 100
i = 5
str_bs = '000000000000000000'
str_num = '100000000000000000000'
ws = gd/2 - 1
min_str = str_num[:ws]
max_str = str_num[:ws+1]
min_num = int(min_str) + num
max_num = int(max_str) - 1
all_the_text = ''
#随机取两位数
one = random.randint(10, 99)
#被10除求商和玉树
int_one = one // 10
int_two = one % 10
sj = random.randint(min_num, max_num)
str1 = str(sj)
code = (str_bs+str(i))
cd = 0-(ws - len(str(kh)))
str2 = str(kh)+code[cd:]
str3 = ''
for j in range(0, gd/2-1):
    if int_one % 2 == 0:
        str3 = str3 + str1[j] + str2[j]
    else:
        str3 = str3 + str2[j] + str1[j]
int_end = int_two - gd + 2
str3 = str3[int_end:] + str3[:int_two]
str4 = str(one) + str3
all_the_text = all_the_text + str4
print all_the_text
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: