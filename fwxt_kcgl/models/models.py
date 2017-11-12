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
import random
import jiemi
date_ref = datetime.now().strftime('%Y-%m-%d')
date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
_logger = logging.getLogger(__name__)



#仓库管理
class warehouse_info(models.Model):
    _name = 'warehouse.info'
    _description = 'warehouse.info'

    code = fields.Char(string='Code', size=64, required=True, help='Code')
    name = fields.Char(string='Name', size=64, required=True, help='Name')
    sf_default = fields.Boolean(string='Default')
    messages = fields.Char(string='Messages', help='Messages')
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help='Date')

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'warehouse.info'),
        'date_confirm': lambda self, cr, uid, context={}: context.get('date', time.strftime("%Y-%m-%d")),
        'user_id': lambda cr, uid, id, c={}: id,
        'sf_default': False
    }

# 库存单据
class warehouse_doc(models.Model):
    _name = 'warehouse.doc'
    _description = 'warehouse.doc'

    code = fields.Char(string='Code', size=64, required=True, help='Code')
    name = fields.Char(string='Name', size=64, required=True, help='Name')
    type = fields.Selection([('in', 'In'),
                             ('out', 'Out'),
                             ('move', 'Move'),
                             ('manual', 'Manual')], 'Type', required=True, help='type')
    batch_id = fields.Many2one('commodity.batch', string='Commodity Batch', help='Commodity Batch')
    commodity_id = fields.Many2one('commodity.info', string='Commodity', help='Commodity')
    warehouse_id = fields.Many2one('warehouse.info', string='Warehouse', help='Warehouse')
    unit_id = fields.Many2one('base.unit', string='Unit')
    line_id = fields.One2many('warehouse.line', 'line_id', string='明细', copy=True)
    agent_id = fields.Many2one('agent.info', string='Agent', help='Agent')
    express_id = fields.Many2one('express.info', string='Express', help='Express')
    express_code = fields.Char(string='Express Code', help='Express Code')
    number = fields.Float(string='Num', help='Num')
    messages = fields.Char(string='Messages', help='Messages')
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help='Date')

    @api.one
    @api.onchange('batch_id')
    def onchange_batch_id(self):
        self.commodity_id = self.batch_id.commodity_id
    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'warehouse.doc'),
        'date_confirm': lambda self, cr, uid, context={}: context.get('date', time.strftime("%Y-%m-%d")),
        'user_id': lambda cr, uid, id, c={}: id,
        'type': lambda obj, cr, uid, context: context['type'],
    }

class warehouse_line(models.Model):
    _name = 'warehouse.line'
    _description = 'warehouse.line'

    code = fields.Char(string='Code', size=64, help='Code')
    name = fields.Char(string='Name', size=64, help='Name')
    line_id = fields.Many2one('warehouse.doc', string='Warehouse Doc')
    warehouse_two_id = fields.Many2one('warehouse.two', string='箱号id')
    start_code = fields.Char(string='Code', size=64, help='Code')
    end_code = fields.Char(string='Code', size=64, help='Code')
    type = fields.Selection([('in', 'In'),
                             ('out', 'Out'),
                             ('move', 'Move'),
                             ('manual', 'Manual')], 'Type', required=True, help='type')
    number = fields.Float(string='Number')
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help='Date')

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'warehouse.line'),
        'date_confirm': lambda self, cr, uid, context={}: context.get('date', time.strftime("%Y-%m-%d")),
        'user_id': lambda cr, uid, id, c={}: id,
        'type': lambda obj, cr, uid, context: context['type'],
    }

class warehouse_one(models.Model):
    _name = 'warehouse.one'
    _description = 'warehouse.one'

    name = fields.Char(string='托盘编号', size=64, help='托盘编号')
    line_id = fields.Many2one('warehouse.doc', string='入库编号')
    start_code = fields.Char(string='开始编号', size=64, help='开始编号')
    end_code = fields.Char(string='结束编号', size=64, help='结束编号')
    type = fields.Selection([('in', 'In'),
                             ('out', 'Out'),
                             ('move', 'Move'),
                             ('manual', 'Manual')], 'Type', required=True, help='type')
    number = fields.Float(string='数量')

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'warehouse.one'),
        'type': lambda obj, cr, uid, context: context['type'],
    }
class warehouse_two(models.Model):
    _name = 'warehouse.two'
    _description = 'warehouse.two'

    name = fields.Char(string='箱编号', size=64, help='箱编号')
    line_id = fields.Many2one('warehouse.doc', string='入库编号')
    warehouse_one_id = fields.Many2one('warehouse.one', string='托盘id')
    start_code = fields.Char(string='开始编号', size=64, help='开始编号')
    end_code = fields.Char(string='结束编号', size=64, help='结束编号')
    type = fields.Selection([('in', 'In'),
                             ('out', 'Out'),
                             ('move', 'Move'),
                             ('manual', 'Manual')], '类型', required=True, help='type')
    number = fields.Float(string='数量')

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'warehouse.two'),
        'type': lambda obj, cr, uid, context: context['type'],
    }

class batch_list(models.Model):
    _name = 'batch.list'
    _description = 'batch.list'

    code = fields.Char(string='Code', size=64, help='Code')
    name = fields.Char(string='Batch Code', size=64, help='Batch Code')
    line_id = fields.Many2one('warehouse.doc', string='Warehouse Doc')
    out_id = fields.Many2one('warehouse.doc', string='Warehouse Doc')
    number = fields.Float(string='number')
    first_date = fields.Datetime(string='Date', size=64, help='Date')
    new_date = fields.Datetime(string='最近时间', size=64, help='最近时间')
    messages = fields.Char(string='Messages', help='Messages')
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help='Date')

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'batch.list'),
        'date_confirm': lambda self, cr, uid, context={}: context.get('date', time.strftime("%Y-%m-%d")),
        'first_date': lambda self, cr, uid, context={}: context.get('date', time.strftime("%Y-%m-%d %H:%M:%S")),
        'user_id': lambda cr, uid, id, c={}: id,
    }

class manual_storage(models.Model):
    _name = 'manual.storage'
    _description = 'manual.storage'

    code = fields.Char(string='编号', size=64, required=True, help='编号')
    name = fields.Char(string='名称', size=64, required=True, help='名称')
    state_code = fields.Char(string='起始号', size=64, required=True, help='起始号')
    batch_id = fields.Many2one('commodity.batch', string='商品批次', help='商品批次')
    commodity_id = fields.Many2one('commodity.info', string='商品', help='商品')
    warehouse_id = fields.Many2one('warehouse.info', string='仓库', help='仓库')
    unit_id = fields.Many2one('base.unit', string='单位')
    number = fields.Float(string='Num', digits=(16, 0), help='数量')
    messages = fields.Char(string='备注', help='备注')
    user_id = fields.Many2one('res.users', string='操作人')
    date_confirm = fields.Date(string='Date', size=64, required=True, help='日期')

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
            'type': 'in',
            'batch_id': str(self.batch_id.id),
            'commodity_id': str(self.commodity_id.id),
            'warehouse_id': str(self.warehouse_id.id),
            'unit_id': str(self.unit_id.id),
            'number': self.number,
            'messages': u'手动入库',
        }
        num = int(self.number)
        rk_obj_id = self.env['warehouse.doc'].create(values)
        state_code = self.state_code
        state_number = jiemi.def_jiemi(state_code)
        str_code = '000000000000000000000' + str(int(state_number) + num - 1)
        end_number = str_code[0-len(state_number):]
        values = {
            'code': state_code,
            'name': state_code,
            'type': 'in',
            'start_code': state_number,
            'end_code': end_number,
            'line_id': str(rk_obj_id.id),
            'number': num,
        }
        id = self.env['warehouse.line'].create(values)
        return {'type': 'ir.actions.act_window_close'}

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'manual.storage'),
        'number': 1,
        'to_batch': 0,
        'from_batch': 0,
        'date_confirm': lambda self, cr, uid, context={}: context.get('date', time.strftime("%Y-%m-%d")),
        'user_id': lambda cr, uid, id, c={}: id,
    }
    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: