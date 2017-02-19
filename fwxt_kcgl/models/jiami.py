# -*- coding: utf-8 -*-
import random
def def_jiami(int_num,str_kh):
    code = '0000000000000000'+str(int_num)
    code = code[-8:]
    num = int(int_num)
    kh =str_kh
    gd = len(str(code))
    #随机取两位数
    one = random.randint(10, 99)
    #求10的商和余数
    int_one = one // 10
    int_two = one % 10
    #随机取8位数
    sj = random.randint(10000000, 99999999)
    #转换程字符床
    str1 = str(sj)
    #加上客户数字 凑齐8位 不够的中间补0
    str2 = code
    str3 = ''
    #根据随机的二位树 第一位是奇数还是偶数
    for j in range(0, gd):
        if int_one % 2 == 0:
            str3 = str3 + str1[j] + str2[j]
        else:
            str3 = str3 + str2[j] + str1[j]
    #根据随机的二位数，惊醒左右转换
    str3 = str(kh) + str3
    int_end = int_two - len(str3)
    # print int_two,int_end,str3
    str3 = str3[int_end:] + str3[:int_two]
    str4 = str(one) + str3
    return str4
# int_num = 101
# str_kh = 22
# str = def_jiami(int_num, str_kh)
# print str
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: