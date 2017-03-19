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
import jiami
import jiemi
import os
date_ref = datetime.now().strftime('%Y-%m-%d')
_logger = logging.getLogger(__name__)
class fwxt_company(models.Model):
    _name = "fwxt.company"
    _description = "fwxt.company"

    code = fields.Char(string='编号', size=64, help="编号")
    name = fields.Char(string='客户名称', help="客户名称")
    company_code = fields.Char(string='客户数字', help="客户数字")
    state_number = fields.Integer(string='当前序号', help="当前序号")
    messages = fields.Char(string='备注', help="备注")
    user_id = fields.Many2one('res.users', string='录入人')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="录入日期")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'fwxt.company'),
        'date_confirm': date_ref,
        'state_number': 1,
        'user_id': lambda cr, uid, id, c={}: id,
    }
class fwxt_create(models.Model):
    _name = 'fwxt.create'
    _description = 'fwxt.create'

    code = fields.Char(string='编号', size=64, help='编号')
    name = fields.Char(string='名称', size=64, help='名称')
    company_id = fields.Many2one('fwxt.company', required=True, string='客户名称')
    company_code = fields.Char(string='客户数字', size=64, help='客户数字')
    state_number = fields.Char(string='开始序号', size=64, help='开始序号')
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
        self.state_number = self.company_id.state_number
    @api.one
    def btn_create(self):
        #加密算发
        comany = self.company_id.name
        save = '/home/ftp' + comany + date_ref + '.txt'
        file_object = open(save, 'w')
        file_object.write('')
        file_object.close()
        kh = self.company_code
        num = self.number
        all_the_text = ''
        for i in range(1, num + 1):
            str4 = jiami.def_jiami(i, kh)
            num = num + 1
            all_the_text = all_the_text + str4 + '\n'
            if num == 1000:
                file_object = open(save, 'a')
                file_object.write(all_the_text)
                file_object.close()
                all_the_text = ''
                num = 0
        if num > 0:
            file_object = open(save, 'a')
            file_object.write(all_the_text)
            file_object.close()
            comany_objs = self.env['fwxt.company']
            comany_obj = comany_objs.search([('id', '=', self.company_id.id)])
            if comany_obj:
                comany_obj.update({'state_number': self.state_number + num})

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
        b1 = jiemi.def_jiemi(code)
        self.decrypt_code = b1
    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: