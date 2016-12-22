# -*- coding: utf-8 -*-
import random
code = '3182136060107921'
code = str(code)
str_one = code[:2]
print str_one
str_len = 2 - len(code)
print str_len
str_code = code[str_len:]
print str_code
int_one = int(str_one) // 10
int_two = int(str_one) % 10
int_end = len(code) - int_two
b1 = ''
print str_code ,int_one ,int_two,int_end
str_code = str_code[0-int_two:] + str_code[:int_end]
print str_code
if int_one % 2 == 0:
    for i in range(1, len(code)-2, 2):
        b1 = b1 + str_code[i]
else:
    for i in range(0, len(code)-2, 2):
        b1 = b1 + str_code[i]
print b1


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: