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
# -*- coding: utf-8 -*-
import logging
from openerp import fields,models,api
from datetime import datetime
date_ref = datetime.now().strftime('%Y-%m-%d')
_logger = logging.getLogger(__name__)

class company_info(models.Model):
    _name = "company.info"
    _description = "company.info"

    code = fields.Char(string='Code', size=64, required=True, help="No.")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    company_info = fields.Text(string='Company Info', help="Company Info")
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class picture_management(models.Model):
    _name = "picture.management"
    _description = "picture.management"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    type = fields.Selection([('heard', 'Heard'),
                             ('boby', 'Boby'),
                             ('other', 'Other')], 'Picture Type', required=True, help="Picture Type")
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class convert_info(models.Model):
    _name = "convert.info"
    _description = "convert.info"

    code = fields.Char(string='Code', size=64, required=True, help="No.")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    number = fields.Float(string='Number', help="Number")
    convert = fields.Float(string='Convert', help="Convert")
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
class video_info(models.Model):
    _name = "video.info"
    _description = "video.info"

    code = fields.Char(string='Code', size=64, required=True, help="No.")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    tel = fields.Char(string='Tel', help="Tel")
    weixin_add = fields.Char(string='Weixin Add', help="Weixin Add")
    web_add = fields.Char(string='Web add', help="Web add")
    shop_add = fields.Char(string='Shop Add', help="Shop Add")
    Search = fields.Char(string='Search', help="Search")
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class dict_info(models.Model):
    _name = "dict.info"
    _description = "dict.info"

    code = fields.Char(string='Code', size=64, readonly=True, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    type = fields.Selection([('supplier', 'Supplier'),
                             ('dealer','Dealer'),
                             ('distributor','Distributor'),
                             ('detection','Detection'),
                             ('production','Producttion'),
                             ('material','Material'),
                             ('manufacturing','Manufacturing'),
                             ('warehouse','Warehouse')], 'Type', required=True, help="Type")
    dist = fields.Char(string='Dist', help="Dist")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class material_type(models.Model):
    _name = "materia.type"
    _description = "materia.type"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
class material_info(models.Model):
    _name = "materia.info"
    _description = "materia.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    materia_type = fields.Many2one('materia.type', string='Type')
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class branch_office_info(models.Model):
    _name = "branch.office.info"
    _description = "branch.office.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    video_info = fields.Many2one('video.info', string='Video Info')
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class material_info(models.Model):
    _name = "materia.info"
    _description = "materia.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    materia_type = fields.Many2one('materia.type', string='Type')
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class commodity_type(models.Model):
    _name = "commodity.type"
    _description = "commodity.type"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
class commodity_info(models.Model):
    _name = "commodity.info"
    _description = "commodity.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    commodity_type = fields.Many2one('commodity.type', string='Type')
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
class supplier_type(models.Model):
    _name = "supplier.type"
    _description = "supplier.type"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
class supplier_info(models.Model):
    _name = "supplier.info"
    _description = "supplier.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    type = fields.Selection([('supplier', 'Supplier'),
                             ('agent', 'Agent'),
                             ('express', 'Express')], 'Product Type', required=True, help="Type")

    supplier_type = fields.Many2one('supplier.type', string='Type')
    contacts_name = fields.Char(string='Contacts Name', help="Contacts Name")
    tel = fields.Char(string='Tel', help="Tel")
    address = fields.Char(string='Address', size=64, required=True, help="Address")
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
        'type': 'supplier'
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: