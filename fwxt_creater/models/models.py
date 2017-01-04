# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Odoo Connector
# QQ:61365857
# 邮件:caobo@shmingjiang.org.cn
# 手机：15562666538
# 作者：'caobo'
# 公司网址： www.goderp.com
# 山东开源ERP有限公司
# 日期：2015-12-18
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

import logging
from openerp import fields,models,api
from datetime import datetime
import random
import os
date_ref = datetime.now().strftime('%Y-%m-%d')
_logger = logging.getLogger(__name__)
class fwxt_company(models.Model):
    _name = "fwxt.company"
    _description = "fwxt.company"

    code = fields.Char(string='编号', size=64, help="编号")
    name = fields.Char(string='客户名称', help="客户名称")
    company_code = fields.Char(string='客户数字', help="客户数字")
    messages = fields.Char(string='备注', help="备注")
    user_id = fields.Many2one('res.users', string='录入人')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="录入日期")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'fwxt.company'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
class fwxt_create(models.Model):
    _name = 'fwxt.create'
    _description = 'fwxt.create'

    code = fields.Char(string='编号', size=64, help='编号')
    name = fields.Char(string='名称', size=64, help='名称')
    company_id = fields.Many2one('fwxt.company', required=True, string='客户名称')
    company_code = fields.Char(string='客户数字', size=64, help='客户数字')
    end_code1 = fields.Integer(string='尾数1', size=64, help='尾数1')
    end_code2 = fields.Integer(string='尾数2', size=64, help='尾数2')
    end_code3 = fields.Integer(string='尾数3', size=64, help='尾数3')
    fixed_value = fields.Integer(string='固定位数')
    number = fields.Integer(string='数量')
    create_file = fields.Binary(string='附件')
    messages = fields.Char(string='备注', help='备注')
    user_id = fields.Many2one('res.users', string='录入人')
    date_confirm = fields.Date(string='录入日期', size=64, required=True, help='录入日期')

    @api.one
    @api.onchange('company_id')
    def onchange(self):
        self.company_code = self.company_id.company_code
    @api.one
    def btn_create(self):
        #加密算发
        comany = self.company_id.name
        file_object = open('d://' + comany + date_ref + '.txt', 'w')
        file_object.write('')
        file_object.close()
        kh = self.company_code
        gd = self.fixed_value
        num = self.number
        str_bs = '000000000000000000'
        str_num = '100000000000000000000'
        ws = gd/2 - 1
        min_str = str_num[:ws]
        max_str = str_num[:ws+1]
        min_num = int(min_str) + num
        max_num = int(max_str) - 1
        all_the_text = ''
        for i in range(1, num + 1):
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
            code = (str_bs+str(i))
            cd = 0-(ws - len(str(kh)))
            str2 = str(kh)+code[cd:]
            str3 = ''
            #根据随机的二位树 第一位是奇数还是偶数
            for j in range(0, gd/2-1):
                if int_one % 2 == 0:
                    str3 = str3 + str1[j] + str2[j]
                else:
                    str3 = str3 + str2[j] + str1[j]
            #根据随机的二位数，惊醒左右转换
            int_end = int_two - gd + 2
            str3 = str3[int_end:] + str3[:int_two]
            str4 = str(one) + str3
            num = num + 1
            all_the_text = all_the_text + str4 +'\n'
            if num == 100:
                file_object = open('c://' + comany + date_ref + '.txt', 'a')
                file_object.write(all_the_text)
                file_object.close()
                all_the_text = ''
                num = 0
        if num > 0:
            file_object = open('c://' + comany + date_ref + '.txt', 'a')
            file_object.write(all_the_text)
            file_object.close()

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'fwxt.create'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c = {}: id,
    }
class fwxt_decrypt(models.Model):
    _name = "fwxt.decrypt"
    _description = "fwxt.decrypt"

    name = fields.Char(string='条形码', size=64, help="条形码")
    decrypt_code = fields.Char(string='解密', size=64, help="解密")
    company_id = fields.Many2one('fwxt.company', string='客户名称')
    messages = fields.Char(string='备注', help="备注")
    user_id = fields.Many2one('res.users', string='操作人')
    date_confirm = fields.Date(string='录入日期', size=64, required=True, help="录入日期")

    @api.one
    def btn_decrypt(self):
        code = self.name
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
        self.decrypt_code = b1
    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: