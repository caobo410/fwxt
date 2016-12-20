# -*- coding: utf-8 -*-
import random
code = '9152734099298481'
code = str(code)
str_one = code[:2]
str_len = 2 - len(code)
str_code = code[str_len:]
int_one = int(str_one) // 10
int_two = int(str_one) % 10
int_end = len(code) - int_two
b1 = ''
str_code = str_code[0-int_two:] + str_code[:int_end]
if int_one % 2 == 0:
    for i in range(1, len(code)-2, 2):
        b1 = b1 + str_code[i]
else:
    for i in range(0, len(code)-2, 2):
        b1 = b1 + str_code[i]
print b1


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: