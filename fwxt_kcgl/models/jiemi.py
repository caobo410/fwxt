# -*- coding: utf-8 -*-
import random
def def_jiemi(str_code):
    code = str_code
    code = str(code)
    str_one = code[:2]
    # print str_one
    str_len = 2 - len(code)
    str_code = code[str_len:]
    int_one = int(str_one) // 10
    int_two = int(str_one) % 10
    int_end = len(code) - 2 - int_two
    b1 = ''
    # print str_code, int_one , int_two, int_end
    if int_two == 0:
        str_code = str_code
    else:
        str_code = str_code[0-int_two:] + str_code[:int_end]
    # print str_code
    str_code = str_code[2-len(str_code):]
    # print str_code
    if int_one % 2 == 0:
        for i in range(1, len(str_code), 2):
            b1 = b1 + str_code[i]
    else:
        for i in range(0, len(str_code), 2):
            b1 = b1 + str_code[i]
    return b1

def def_company(str_code):
    code = str_code
    code = str(code)
    str_one = code[:2]
    # print str_one
    str_len = 2 - len(code)
    str_code = code[str_len:]
    int_one = int(str_one) // 10
    int_two = int(str_one) % 10
    int_end = len(code) - 2 - int_two
    b1 = ''
    # print str_code, int_one , int_two, int_end
    if int_two == 0:
        str_code = str_code
    else:
        str_code = str_code[0 - int_two:] + str_code[:int_end]
    # print str_code
    str_code = str_code[:2]
    return str_code
# code = '80437010503040702105'
# srt = def_company(code)
# print srt
# code ='79093989491430508199'

    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: