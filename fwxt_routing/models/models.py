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

#工艺路线
class base_routing(models.Model):
    _name = "base.routing"
    _description = "base.routing"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    line_id = fields.One2many('routing.line', 'line_id', string='join', copy=True)
    picture_id = fields.Many2one('picture.management', string='Picture', select=True, track_visibility='onchange')
    video_id = fields.Many2one('ir.attachment', string='Video', select=True, track_visibility='onchange')
    messages = fields.Text(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'base.routing'),
        'date_confirm': lambda self, cr, uid, context={}: context.get('date', time.strftime("%Y-%m-%d")),
        'user_id': lambda cr, uid, id, c={}: id,
    }

#工艺路线子项
class routing_line(models.Model):
    _name = "routing.line"
    _description = "routing.line"

    line_id = fields.Many2one('base.routing', string='join', select=True, track_visibility='onchange')
    step_id = fields.Many2one('base.step', string='Step', select=True, track_visibility='onchange')
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    messages = fields.Char(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    @api.one
    @api.onchange('step_id')
    def onchange_step_id(self):
        if self.step_id:
            self.name = self.step_id.code + ' ' + self.step_id.name

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'routing.line'),
        'date_confirm': lambda self, cr, uid, context={}: context.get('date', time.strftime("%Y-%m-%d")),
        'user_id': lambda cr, uid, id, c={}: id,
    }

#工序
class base_step(models.Model):
    _name = "base.step"
    _description = "base.step"

    code = fields.Char(string='Code', size=64, required=True, help="Code")
    name = fields.Char(string='Name', size=64, required=True, help="Name")
    picture_id = fields.Many2one('picture.management', string='Picture', select=True, track_visibility='onchange')
    video_id = fields.Many2one('ir.attachment', string='Video', select=True, track_visibility='onchange')
    messages = fields.Text(string='Messages', help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'base.step'),
        'date_confirm': lambda self, cr, uid, context={}: context.get('date', time.strftime("%Y-%m-%d")),
        'user_id': lambda cr, uid, id, c={}: id,
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: