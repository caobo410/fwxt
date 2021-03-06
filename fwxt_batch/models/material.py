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
import time

_logger = logging.getLogger(__name__)

class material_batch(models.Model):
    _name = 'material.batch'
    _description = 'material.batch'

    code = fields.Char(string='Code', size=64, required=True, help='Code')
    name = fields.Char(string='Name', size=64, required=True, help='Name')
    batch = fields.Char(string='Batch', size=64, required=True, help='Batch')
    picture_id = fields.Many2one('picture.management', string='Picture')
    file_id = fields.Many2one('ir.attachment', string='File')
    materia_id = fields.Many2one('materia.info', string='Materia Info')
    supplier_id = fields.Many2one('supplier.info', string='Supplier Info', help='Supplier')
    # material_batch_id = fields.Many2one('commodity.batch', string='Commodity Batch', help='Supplier')
    production_date = fields.Date(string='生产日期', size=64, required=True, help='生产日期')
    number = fields.Float(string='Num')
    unit_id = fields.Many2one('base.unit', string='Unit')
    messages = fields.Char(string='Messages', help='Messages')
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help='Date')

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for account in self:
            name = account.batch + ' ' + account.name
            result.append((account.id, name))
        return result

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'material.batch'),
        'production_date': lambda self, cr, uid, context={}: context.get('date', time.strftime("%Y-%m-%d")),
        'date_confirm': lambda self, cr, uid, context={}: context.get('date', time.strftime("%Y-%m-%d")),
        'user_id': lambda cr, uid, id, c={}: id,
    }

class commodity_batch(models.Model):
    _name = 'commodity.batch'
    _description = 'commodity.batch'

    code = fields.Char(string='Code', size=64, required=True, help='Code')
    name = fields.Char(string='酒罐编号', size=64, required=True, help='酒罐编号')
    batch = fields.Char(string='Batch', size=64, required=True, help='Batch')
    commodity_id = fields.Many2one('commodity.info', string='Commodity')
    line_id = fields.One2many('commodity.batch.line', 'line_id', string='join', copy=True)
    branch_id = fields.Many2one('branch.office.info', string='Branch Office', select=True, track_visibility='onchange')
    production_date = fields.Date(string='生产日期', size=64, required=True, help='生产日期')
    messages = fields.Char(string='生产线号', help='生产线号')
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help='Date')

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for account in self:
            name = account.batch + ' ' + account.name
            result.append((account.id, name))
        return result

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'commodity.batch'),
        'production_date': lambda self, cr, uid, context={}: context.get('date', time.strftime("%Y-%m-%d")),
        'date_confirm': lambda self, cr, uid, context={}: context.get('date', time.strftime("%Y-%m-%d")),
        'user_id': lambda cr, uid, id, c={}: id,
    }
class commodity_batch_line(models.Model):
    _name = 'commodity.batch.line'
    _description = 'commodity.batch.line'

    line_id = fields.Many2one('commodity.batch', string='Commodity Batch', select=True, track_visibility='onchange')
    material_batch_id = fields.Many2one('material.batch', string='Batch', select=True, track_visibility='onchange')
    name = fields.Char(string='Name', size=64, required=True, help='Name')
    messages = fields.Char(string='Messages', help='Messages')
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help='Date')

    @api.one
    @api.onchange('material_batch_id')
    def onchange_material_batch_id(self):
        self.name = self.material_batch_id.name

    _defaults = {
        'date_confirm': lambda self, cr, uid, context={}: context.get('date', time.strftime("%Y-%m-%d")),
        'user_id': lambda cr, uid, id, c={}: id,
    }




    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: