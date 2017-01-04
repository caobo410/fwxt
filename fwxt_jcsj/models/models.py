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


def _get_select_materia_types(self):
    return self.pool.get('dict.info').get_selection_type_items('material', self._cr, self._uid)

def _get_select_commodity_types(self):
    return self.pool.get('dict.info').get_selection_type_items('commodity', self._cr, self._uid)

def _get_select_supplier_types(self):
    return self.pool.get('dict.info').get_selection_type_items('supplier', self._cr, self._uid)


#字典查询下拉菜单


#企业信息
class company_info(models.Model):
    _name = "company.info"
    _description = "company.info"

    code = fields.Char(string='Code', size=64, required=True, help="No.")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    company_code = fields.Char(string='Company Code', size=64, required=True, help="Company Code")
    company_info = fields.Text(string='Company Info', help="Company Info")
    contacts_people = fields.Char(string='Contacts', help="Contacts")
    tel = fields.Char(string='Tel', help="Tel")
    wetch = fields.Char(string='Wetch', help="Wetch")
    qq = fields.Char(string='QQ', help="QQ")
    address = fields.Char(string='Address', help="Address")
    website = fields.Char(string='WebSite', help="WebSite")
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'company.info'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

#照片管理
class picture_management(models.Model):
    _name = "picture.management"
    _description = "picture.management"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    type = fields.Selection([('head', 'Head'),
                             ('boby', 'Boby'),
                             ('other', 'Other')], 'Picture Type', required=True, help="Picture Type")
    image = fields.Binary(string='Image', help='Image')
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'picture.management'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

# 单位
class base_unit(models.Model):
    _name = "base.unit"
    _description = "base.unit"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'base.unit'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

#单位换算
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
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'convert.info'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }



#其他设置
class other_info(models.Model):
    _name = "other.info"
    _description = "other.info"

    code = fields.Char(string='Code', size=64, required=True, help="No.")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    tel = fields.Char(string='Tel', help="Tel")
    password = fields.Char(string='Check Password', help="Check Password")
    web_add = fields.Char(string='Web add', help="Web add")
    shop_add = fields.Char(string='Shop Add', help="Shop Add")
    wechat_account =fields.Char(string='Wechat Account', help="Wechat Account")
    Search = fields.Text(string='Search', help="Search")
    search_two = fields.Text(string='Search Two', help="Search Two")
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'other.info'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

#字典信息
class dict_info(models.Model):
    _name = "dict.info"
    _description = "dict.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    type = fields.Selection([('material', 'Material'),
                             ('supplier', 'Supplier'),
                             ('agent', 'Agent'),
                             ('express', 'Express'),
                             ('check', 'Check'),
                             ('commodity', 'Cmmodity'),
                             ('produce', 'Produce'),
                             ('making', 'Making'),
                             ('video', 'Video')], 'Type', required=True, help="Type")
    dict = fields.Char(string='Dict', help="Dict")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    def get_selection_type_items(self, type, cr, uid):
        dicts = self.search(cr, uid, [('type', '=', type)])
        if not len(dicts):
            return []
        ret_list = []
        for dict in dicts:
            item = self.browse(cr, uid, dict)
            ret_list.extend([(item.code, item.name)])
        return ret_list

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'dict.info'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

#附件管理
class ir_attachment(models.Model):
    _inherit = 'ir.attachment'

    code = fields.Char(string='Code', help='Code')
    video_type = fields.Many2one('dict.info', string="Type", domain="[('type', '=', 'video')]")
# 生产基地
class branch_office_info(models.Model):
    _name = "branch.office.info"
    _description = "branch.office.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    other_id = fields.Many2one('ir.attachment', string='Video Info')
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'branch.office.info'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }


#原材料
class material_info(models.Model):
    _name = "materia.info"
    _description = "materia.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    type = fields.Selection(selection=_get_select_materia_types, string='Type', required=True)
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'materia.info'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

#成品商品
class commodity_info(models.Model):
    _name = "commodity.info"
    _description = "commodity.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    type = fields.Selection(selection=_get_select_commodity_types, string='Type', required=True)
    image = fields.Binary(string="Image", help="This field holds the image used as image for the product, limited to 300x300px.")
    routing_id = fields.Many2one('base.routing', string='Routing', select=True, track_visibility='onchange')
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    line_id = fields.One2many('commodity.line', 'line_id', string='join', copy=True)
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'commodity.info'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
#产品说明
class commodity_line(models.Model):
    _name = "commodity.line"
    _description = "commodity.line"

    code = fields.Char(string='No.', size=64, required=True, help="No.")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    line_id = fields.Many2one('commodity.info', string='Commodity Info', select=True, track_visibility='onchange')
    messages = fields.Text(string='Messages', help="Messages")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'commodity.line'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
#供应商
class supplier_info(models.Model):
    _name = "supplier.info"
    _description = "supplier.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    type = fields.Many2one('dict.info', string='Area', domain=[('type', '=', 'supplier')], required=True, select=True, track_visibility='onchange')
    contacts_name = fields.Char(string='Contacts Name', help="Contacts Name")
    tel = fields.Char(string='Tel', help="Tel")
    address = fields.Char(string='Address', size=64, help="Address")
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'supplier.info'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

#经销商
class agent_info(models.Model):
    _name = "agent.info"
    _description = "agent.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    type = fields.Many2one('dict.info', string='Type', domain=[('type', '=', 'agent')], required=True, select=True, track_visibility='onchange')
    contacts_name = fields.Char(string='Contacts Name', help="Contacts Name")
    tel = fields.Char(string='Tel', help="Tel")
    area = fields.Char(string='area', help="area")
    address = fields.Char(string='Address', size=64, help="Address")
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'agent.info'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

#配送公司
class express_info(models.Model):
    _name = "express.info"
    _description = "express.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    type = fields.Many2one('dict.info', string='Type', domain=[('type', '=', 'express')], required=True, select=True, track_visibility='onchange')
    contacts_name = fields.Char(string='Contacts Name', help="Contacts Name")
    tel = fields.Char(string='Tel', help="Tel")
    address = fields.Char(string='Address', size=64, help="Address")
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'express.info'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

#质检公司
class check_info(models.Model):
    _name = "check.info"
    _description = "check.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    type = fields.Many2one('dict.info', string='Type', domain=[('type', '=', 'check')], required=True, select=True, track_visibility='onchange')
    contacts_name = fields.Char(string='Contacts Name', help="Contacts Name")
    tel = fields.Char(string='Tel', help="Tel")
    address = fields.Char(string='Address', size=64, help="Address")
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'check.info'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: