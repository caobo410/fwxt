# -*- coding: utf-8 -*-
import time
import random
code = [[0] * 10] * 5
code[0] = ['7', '8', '6', '2', '4', '3', '5', '1', '0', '9']
code[1] = ['3', '9', '4', '1', '5', '8', '0', '6', '7', '2']
code[2] = ['9', '7', '2', '0', '5', '8', '1', '3', '4', '6']
code[3] = ['7', '3', '9', '1', '0', '6', '5', '2', '4', '8']
code[4] = ['6', '7', '0', '9', '3', '2', '1', '4', '8', '5']
#str_num :最大位数的自负成如：00001， int_time 当前时间 转换成 int
def def_jiami(str_num, int_time):
    num = str_num
    a = int_time
    bit = len(str(num))
    oct_str = str(oct(a))
    oct_str = str(oct(a))
    oct_str = oct_str.replace('L', '')
    # oct_str = oct_str[:len(oct_str)]
    if len(str_num) == 6:
        len_num = 21 - bit
    else:
        len_num = 23 - bit
    n = 1
    while n < len_num:
        ran = random.randint(0, len(oct_str) - 1)
        oct_str = oct_str[:ran] + '9' + oct_str[ran-len(oct_str):]
        n = len(oct_str)
    out = str(bit) + oct_str + str(num)
    out_len = len(out)
    i = 0
    sum = 0
    while i <= out_len - 1:
        sum = sum + int(out[i])
        i = i + 1
    out = str(sum % 10) + out
    out = out[10-len(out):] + out[:10]
    print_out = ''
    len_out = len(out)
    for i in range(0, 5):
        for j in range(0, 5):
            index = i * 5 + j
            if index > len_out - 1:
                return print_out
            flag_int = int(out[index])
            print_out = print_out + code[i][flag_int]
    return print_out
#
# a = def_jiami('000001', 1493563337)
# print a

# 8299962169999975687397556
# 82912 26933 99748 78318 765
# 92912 69333 99791 78313 657
# 99129 69333 99777 04731 75679

