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

class material_barch(models.Model):
    _name = "material.barch"
    _description = "material.barch"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    barch = fields.Char(string='Barch', size=64, required=True, help="Barch")
    materia_id = fields.Many2one('materia.info', string='Materia Info')
    supplier_id = fields.Many2one('supplier.info', string='Supplier Info', domain=[('type', '=', 'supplier')], help="Supplier")
    commodity_barch_id = fields.Many2one('commodity.barch', string='Commodity Barch')
    production_date = fields.Date(string='Date', size=64, required=True, help="Date")
    messages = fields.Char(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for account in self:
            name = account.barch + ' ' + account.name
            result.append((account.id, name))
        return result

    _defaults = {
        'production_date': date_ref,
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class commodity_barch(models.Model):
    _name = "commodity.barch"
    _description = "commodity.barch"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    barch = fields.Char(string='Barch', size=64, required=True, help="Barch")
    commodity_id = fields.Many2one('commodity.info', string='Commodity')
    # supplier_id = fields.Many2one('supplier.info', string='Supplier Info', domain=[('type', '=', 'supplier')], help="Supplier")
    material_barch_id = fields.One2many('material.barch', 'commodity_barch_id', string='join')
    production_date = fields.Date(string='Date', size=64, required=True, help="Date")
    messages = fields.Char(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")


    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for account in self:
            name = account.barch + ' ' + account.name
            result.append((account.id, name))
        return result

    _defaults = {
        'production_date': date_ref,
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: