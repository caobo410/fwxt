# -*- coding: utf-8 -*-
import random
code='1230000'
num = 1
kh ='123'
gd = len(str(code))
str_bs = '000000000000000000'
str_num = '100000000000000000000'
ws = gd
min_str = str_num[:ws]
max_str = str_num[:ws+1]
min_num = int(min_str) + num
max_num = int(max_str) - 1
#随机取两位数
one = random.randint(10, 99)
#求10的商和余数
int_one = one // 10
int_two = one % 10
#随机取8位数
sj = random.randint(min_num, max_num)
#转换程字符床
str1 = str(sj)
#加上客户数字 凑齐8位 不够的中间补0
str_code = (str_bs+str(num))
cd = 0-(ws - len(str(kh)))
str2 = str(kh)+str_code[cd:]
str3 = ''
#根据随机的二位树 第一位是奇数还是偶数
for j in range(0, gd):
    if int_one % 2 == 0:
        str3 = str3 + str1[j] + str2[j]
    else:
        str3 = str3 + str2[j] + str1[j]
#根据随机的二位数，惊醒左右转换
int_end = int_two - gd*2
str3 = str3[int_end:] + str3[:int_two]
str4 = str(one) + str3
print '9323 7090 0021 4112'
print str4

# code = str('97403841428370')
# str_one = code[:2]
# str_len = 2 - len(code)
# str_code = code[str_len:]
# int_one = int(str_one) // 10
# int_two = int(str_one) % 10
# int_end = len(code) - int_two
# b1 = ''
# str_code = str_code[0-int_two:] + str_code[:int_end]
# if int_one % 2 == 0:
#     for i in range(1, len(code)-2, 2):
#         b1 = b1 + str_code[i]
# else:
#     for i in range(0, len(code)-2, 2):
#         b1 = b1 + str_code[i]
# print b1
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: