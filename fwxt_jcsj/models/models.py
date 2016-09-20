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
    company_info = fields.Text(string='Company Info', help="Company Info")
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

#照片管理
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
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

#视频管理
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

#字典信息
class dict_info(models.Model):
    _name = "dict.info"
    _description = "dict.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    type = fields.Selection([('material', 'Material'),
                             ('supplier', 'Supplier'),
                             ('commodity', 'Cmmodity'),
                             ('produce', 'Produce'),
                             ('making', 'Making')], 'Type', required=True, help="Type")
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
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

# 生产基地
class branch_office_info(models.Model):
    _name = "branch.office.info"
    _description = "branch.office.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    video_id = fields.Many2one('video.info', string='Video Info')
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
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
    message = fields.Char(string='Message', help="Message")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

#供应商
class supplier_info(models.Model):
    _name = "supplier.info"
    _description = "supplier.info"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    type = fields.Selection([('supplier', 'Supplier'),
                             ('agent', 'Agent'),
                             ('express', 'Express'),
                             ('check', 'Check')], 'Product Type', required=True, help="Type")

    supplier_type = fields.Selection(selection=_get_select_supplier_types, string='Supplier type', required=True)
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