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

#商品生产
class commodity_produce(models.Model):
    _name = "commodity.produce"
    _description = "commodity.produce"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    commodity_id = fields.Many2one('commodity.info', string='Commodity')
    line_id = fields.One2many('produce.line', 'line_id', string='list', copy=True)
    picture_id = fields.Many2one('picture.management', string='Picture')
    video_id = fields.Many2one('ir.attachment', string='Video')
    messages = fields.Char(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'commodity.produce'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class produce_line(models.Model):
    _name = "produce.line"
    _description = "produce.line"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    picture_id = fields.Many2one('picture.management', string='Picture')
    video_id = fields.Many2one('ir.attachment', string='Video')
    line_id = fields.Many2one('commodity.produce', string='Commodity Produce', select=True, track_visibility='onchange')
    type = fields.Many2one('dict.info', string='Type', domain=[('type', '=', 'produce')])
    messages = fields.Text(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'produce.line'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

#商品加工
class commodity_making(models.Model):
    _name = "commodity.making"
    _description = "commodity.making"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    picture_id = fields.Many2one('picture.management', string='Picture')
    video_id = fields.Many2one('ir.attachment', string='Video')
    commodity_id = fields.Many2one('commodity.info', string='Commodity')
    line_id = fields.One2many('making.line', 'line_id', string='list', copy=True)
    messages = fields.Text(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'commodity.making'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class making_line(models.Model):
    _name = "making.line"
    _description = "making.line"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    picture_id = fields.Many2one('picture.management', string='Picture')
    video_id = fields.Many2one('ir.attachment', string='Video')
    line_id = fields.Many2one('commodity.making', string='Commodity Making', select=True, track_visibility='onchange')
    type = fields.Many2one('dict.info', string='Type', domain=[('type', '=', 'making')])
    messages = fields.Text(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'making.line'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

#商品质检
class commodity_check(models.Model):
    _name = "commodity.check"
    _description = "commodity.check"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    picture_id = fields.Many2one('picture.management', string='Picture')
    commodity_id = fields.One2many('commodity.check.line', 'commodity_id', string='list', copy=True)
    line_id = fields.One2many('check.line', 'line_id', string='list', copy=True)
    messages = fields.Text(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")
    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'commodity.check'),
        'check_date': date_ref,
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class check_line(models.Model):
    _name = "check.line"
    _description = "check.line"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    picture_id = fields.One2many('check.line.picture', 'picture_id', string='Picture', copy=True)
    # commodity_id = fields.One2many('commodity.check.line', 'commodity_id', string='list', copy=True)
    line_id = fields.Many2one('commodity.check', string='Commodity Check', select=True, track_visibility='onchange')
    type = fields.Many2one('dict.info', string='Type', domain=[('type', '=', 'making')])
    check_date = fields.Date(string='Check Date', size=64, required=True, help="Check Date")
    check_id = fields.Many2one('check.info', string='Check Company')
    user_id = fields.Many2one('res.users', string='Operator', select=True, track_visibility='onchange')
    messages = fields.Text(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'check.line'),
        'check_date': date_ref,
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
class check_line_picture(models.Model):
    _name = "check.line.picture"
    _description = "commodity.check.line"

    name = fields.Many2one('picture.management', string='Picture', select=True, track_visibility='onchange')
    picture_id = fields.Many2one('check.line', string='Commodity', select=True, track_visibility='onchange')

class commodity_check_line(models.Model):
    _name = "commodity.check.line"
    _description = "commodity.check.line"

    name = fields.Many2one('commodity.info', string='Commodity', select=True, track_visibility='onchange')
    commodity_id = fields.Many2one('commodity.check', string='Commodity', select=True, track_visibility='onchange')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: