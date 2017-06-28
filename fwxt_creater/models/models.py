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
import time
import jiami
import jiemi
import os
date_ref = datetime.now().strftime('%Y-%m-%d')
date_time = datetime.now().strftime('%Y%m%d%H%M%S')
_logger = logging.getLogger(__name__)
class fwxt_company(models.Model):
    _name = "fwxt.company"
    _description = "fwxt.company"

    code = fields.Char(string=u'编号', size=64, help=u"编号")
    name = fields.Char(string=u'客户名称', help=u"客户名称")
    company_code = fields.Char(string=u'客户数字', help=u"客户数字")
    state_number = fields.Integer(string=u'当前序号', help=u"当前序号")
    messages = fields.Char(string='备注', help=u"备注")
    user_id = fields.Many2one('res.users', string=u'录入人')
    date_confirm = fields.Date(string=u'录入日期', size=64, required=True, help=u"录入日期")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'fwxt.company'),
        'date_confirm': date_ref,
        'state_number': 1,
        'user_id': lambda cr, uid, id, c={}: id,
    }
class fwxt_create(models.Model):
    _name = 'fwxt.create'
    _description = 'fwxt.create'

    code = fields.Char(string=u'编号', size=64, help=u'编号')
    name = fields.Char(string=u'名称', size=64, help=u'名称')
    company_id = fields.Many2one('fwxt.company', required=True, string=u'客户名称')
    company_code = fields.Char(string=u'客户数字', size=64, help=u'客户数字')
    state_number = fields.Integer(string=u'开始序号', size=64, help=u'开始序号')
    number = fields.Integer(string=u'数量')
    sf_taobiao = fields.Boolean(string=u'是否套标')
    tb_number = fields.Integer(string=u'套标个数')
    create_file = fields.Binary(string=u'附件')
    messages = fields.Char(string=u'备注', help=u'备注')
    user_id = fields.Many2one('res.users', string=u'录入人')
    date_confirm = fields.Date(string=u'录入日期', size=64, required=True, help=u'录入日期')

    @api.one
    @api.onchange('company_id')
    def onchange_company_id(self):
        self.company_code = self.company_id.company_code
        self.state_number = self.company_id.state_number + 1
    @api.one
    def btn_create(self):
        #加密算发
        comany = self.company_id.name
        save = u'F:\\' + comany + date_time + u'.txt'
        # save = u'/home/ftp/' + comany + date_time + u'.txt'
        file_object = open(save, 'w')
        file_object.write('')
        file_object.close()
        kh = self.company_code
        num = self.number
        state_number = self.state_number
        sf_taobiao = self.sf_taobiao
        tb_number = self.tb_number
        all_the_text = ''
        int_time = int(time.time()*100)
        max_len = len(str(num+state_number))
        for i in range(state_number, state_number+num + 1):
            if sf_taobiao is True:
                for j in range(0, tb_number + 1):
                    str_j = '00' + str(j)
                    str_num = '00000000' + str(i) + str_j[-2:]
                    str_num = str_num[0-max_len-2:]
                    str4 = jiami.def_jiami(str_num, int_time)
                    all_the_text = all_the_text + str4 + '\n'
                num = num + 1
                all_the_text = all_the_text + '\n'
            else:
                str_num = '00000000' + str(i)
                str_num = str_num[0-max_len:]
                str4 = jiami.def_jiami(str_num, int_time)
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
                comany_obj.update({'state_number': num})

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'fwxt.create'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c = {}: id,
    }
class fwxt_decrypt(models.Model):
    _name = "fwxt.decrypt"
    _description = "fwxt.decrypt"

    name = fields.Char(string=u'条形码', size=64, help=u"条形码")
    decrypt_code = fields.Char(string=u'解密', size=64, help=u"解密")
    company_id = fields.Many2one('fwxt.company', string=u'客户名称')
    messages = fields.Char(string=u'备注', help=u"备注")
    user_id = fields.Many2one('res.users', string=u'操作人')
    date_confirm = fields.Date(string=u'录入日期', size=64, required=True, help=u"录入日期")

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