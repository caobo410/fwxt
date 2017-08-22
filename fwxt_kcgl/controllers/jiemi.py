# -*- coding: utf-8 -*-
import time
import random
code = [[0] * 10] * 5
code[0] = ['7', '8', '6', '2', '4', '3', '5', '1', '0', '9']
code[1] = ['3', '9', '4', '1', '5', '8', '0', '6', '7', '2']
code[2] = ['9', '7', '2', '0', '5', '8', '1', '3', '4', '6']
code[3] = ['7', '3', '9', '1', '0', '6', '5', '2', '4', '8']
code[4] = ['6', '7', '0', '9', '3', '2', '1', '4', '8', '5']
# 149356333763
# 02130625145303L
# 3399902130692514599303100
# 5963858221907991188860796
def def_jiemi(str_num):
    print_out = ''
    len_out = len(str_num)
    for i in range(0, 5):
            for j in range(0, 5):
                index = i * 5 + j
                if index > len_out -1:
                    j = 5
                else:
                    print_out = print_out + str(code[i].index(str_num[index]))
    out = print_out[-10:] + print_out[:len_out-10]
    i = 1
    sum = 0
    while i <= len_out -1:
        sum = sum + int(out[i])
        i = i + 1
    if out[0] != str(sum % 10):
        return '0000'
    len_num = int(out[1])
    code_num = out[0-len_num:]
    code_time = out[2:len_out-len_num]
    code_time = code_time.replace('9', '')
    fw_time = str(int(code_time, 8))
    if fw_time[:3] != '149':
        return '0000'
    return fw_time + str(code_num)
# a = def_jiemi('8488559333268994487970490')
# print a

# 013101373711
# 26091931013739711000001
# 37397110000012609193101
# 1493563337
# 21291 99333 99721 78381 767

