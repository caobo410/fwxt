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

class commodity_produce(models.Model):
    _name = "commodity.produce"
    _description = "commodity.produce"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    commodity_barch_id = fields.Many2one('commodity.barch', string='Commodity Barch')
    type = fields.Many2one('dict.info', string='Type', domain=[('type', '=', 'produce')])
    produce_messages = fields.Text(string='Produce Messages', help="Produce Messages")
    messages = fields.Text(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class commodity_making(models.Model):
    _name = "commodity.making"
    _description = "commodity.making"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    commodity_barch_id = fields.Many2one('commodity.barch', string='Commodity Barch')
    type = fields.Many2one('dict.info', string='Type', domain=[('type', '=', 'making')])
    making_messages = fields.Text(string='Make Messages', help="Make Messages")
    messages = fields.Text(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class commodity_check(models.Model):
    _name = "commodity.check"
    _description = "commodity.check"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    commodity_barch_id = fields.Many2one('commodity.barch', string='Commodity Barch')
    type = fields.Many2one('dict.info', string='Type', domain=[('type', '=', 'making')])
    check_date = fields.Date(string='Check Date', size=64, required=True, help="Check Date")
    supplier_id = fields.Many2one('supplier.info', string='Check Company', domain=[('type', '=', 'check')])
    check_messages = fields.Text(string='Make Messages', help="Make Messages")
    messages = fields.Text(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'check_date': date_ref,
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: