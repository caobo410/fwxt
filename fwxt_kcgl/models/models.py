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



#仓库设在
class warehouse_info(models.Model):
    _name = "warehouse.info"
    _description = "warehouse.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    sf_default = fields.Boolean(string='Default')
    messages = fields.Char(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
        'sf_default': False
    }

# 库存单据
class warehouse_doc(models.Model):
    _name = "warehouse.doc"
    _description = "warehouse.doc"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    type = fields.Selection([('in', 'In'),
                             ('out', 'Out'),
                             ('move', 'Move')], 'Type', required=True, help="type")
    batch_id = fields.Many2one('commodity.batch', string='Commodity Batch', help="Commodity Batch")
    commodity_id = fields.Many2one('commodity.info', string='Commodity', help="Commodity")
    warehouse_id = fields.Many2one('warehouse.info', string='Warehouse', help="Warehouse")
    unit_id = fields.Many2one('base.unit', string='Unit')
    batch_list = fields.One2many('batch.list', 'line_id', string='明细', copy=True)
    number = fields.Float(string='Num', help='Num')
    messages = fields.Char(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class batch_list(models.Model):
    _name = "batch.list"
    _description = "batch.list"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Batch', size=64, required=True, help="Batch")
    line_id = fields.Many2one('warehouse.doc', string='Warehouse Doc')
    messages = fields.Char(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: