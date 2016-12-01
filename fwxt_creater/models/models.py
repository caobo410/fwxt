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
date_ref = datetime.now().strftime('%Y-%m-%d')
_logger = logging.getLogger(__name__)
class caobo_template(models.Model):
    _name = "fwxt.company"
    _description = "fwxt.company"

    code = fields.Char(string='编号', size=64, help="编号")
    name = fields.Char(string='客户名称', help="客户名称")
    company_code = fields.Char(string='客户数字', help="客户数字")
    messages = fields.Char(string='备注', help="备注")
    user_id = fields.Many2one('res.users', string='录入人')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="录入日期")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
class fwxt_create(models.Model):
    _name = 'fwxt.create'
    _description = 'fwxt.create'

    code = fields.Char(string='编号', size=64, help='编号')
    name = fields.Char(string='名称', size=64, help='名称')
    company_id = fields.Many2one('fwxt.company', string='客户名称')
    company_code = fields.Char(string='客户数字', size=64, help='客户数字')
    end_code = fields.Char(string='尾数', size=64, help='尾数')
    random_number = fields.Integer(string='随机数')
    fixed_value = fields.Integer(string='固定位数')
    price_unit = fields.Integer(string='数量')
    create_file = fields.Binary(string='附件')
    messages = fields.Char(string='备注', help='备注')
    user_id = fields.Many2one('res.users', string='录入人')
    date_confirm = fields.Date(string='Date', size=64, required=True, help='录入日期')

    @api.one
    @api.onchange('company_id')
    def onchange(self):
        self.company_code = self.company_id.company_code

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c = {}: id,
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: