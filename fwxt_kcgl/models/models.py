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



#仓库管理
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
                             ('move', 'Move'),
                             ('manual', 'Manual')], 'Type', required=True, help="type")
    batch_id = fields.Many2one('commodity.batch', string='Commodity Batch', help="Commodity Batch")
    commodity_id = fields.Many2one('commodity.info', string='Commodity', help="Commodity")
    warehouse_id = fields.Many2one('warehouse.info', string='Warehouse', help="Warehouse")
    unit_id = fields.Many2one('base.unit', string='Unit')
    batch_list = fields.One2many('batch.list', 'line_id', string='明细', copy=True)
    agent_id = fields.Many2one('agent.info', string='Agent', help="Agent")
    express_id = fields.Many2one('express.info', string='Express', help="Express")
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
    name = fields.Char(string='Batch Code', size=64, required=True, help="Batch Code")
    line_id = fields.Many2one('warehouse.doc', string='Warehouse Doc')
    messages = fields.Char(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class manual_storage(models.Model):
    _name = "manual.storage"
    _description = "manual.storage"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    batch_id = fields.Many2one('commodity.batch', string='Commodity Batch', help="Commodity Batch")
    commodity_id = fields.Many2one('commodity.info', string='Commodity', help="Commodity")
    warehouse_id = fields.Many2one('warehouse.info', string='Warehouse', help="Warehouse")
    unit_id = fields.Many2one('base.unit', string='Unit')
    from_batch = fields.Char(string='From Batch', digits=(16, 1), required=True, help="From Batch")
    to_batch = fields.Float(string='To Batch', digits=(16, 0), required=True, help="To Batch")
    number = fields.Float(string='Num', digits=(16, 0), help='Number')
    messages = fields.Char(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    @api.one
    @api.onchange('from_batch')
    def onchange_from_batch(self):
        if self.from_batch:
            self.to_batch = float(self.from_batch) + float(self.number)

    @api.multi
    def manual_storage(self):
        values = {
            'code': self.code,
            'name': self.name,
            'type': 'manual',
            'batch_id': str(self.batch_id.id),
            'commodity_id': str(self.commodity_id.id),
            'warehouse_id': str(self.warehouse_id.id),
            'unit_id': str(self.unit_id.id),
            'number': self.number,
             }
        rk_obj_id = self.env['warehouse.doc'].create(values)
        if rk_obj_id:
            i = 0
            for j in range(int(self.from_batch), int(self.to_batch)):
                i = i + 1
                values = {
                    'code': str(i),
                    'name': str(j),
                    'line_id': str(rk_obj_id.id),
                    'messages': ' ',
                    # 'user_id': str(self.user_id.id),
                    # 'date_confirm': self.date_confirm,
                }
                print values
                self.env['batch.list'].create(values)
        return {'type': 'ir.actions.act_window_close'}


    _defaults = {
        'number': 1,
        'to_batch': 0,
        'from_batch': 0,
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: