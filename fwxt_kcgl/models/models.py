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
date_ref = datetime.now().strftime('%Y-%m-%d')
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
        'date_confirm': date_ref,
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
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
        'type': lambda obj, cr, uid, context: context['type'],
    }

class warehouse_line(models.Model):
    _name = 'warehouse.line'
    _description = 'warehouse.line'

    code = fields.Char(string='Code', size=64, help='Code')
    name = fields.Char(string='Name', size=64, help='Name')
    line_id = fields.Many2one('warehouse.doc', string='Warehouse Doc')
    number = fields.Float(string='Number')
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help='Date')

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'warehouse.line'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class batch_list(models.Model):
    _name = 'batch.list'
    _description = 'batch.list'

    code = fields.Char(string='Code', size=64, help='Code')
    name = fields.Char(string='Batch Code', size=64, help='Batch Code')
    line_id = fields.Many2one('warehouse.doc', string='Warehouse Doc')
    number = fields.Float(string='number')
    messages = fields.Char(string='Messages', help='Messages')
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help='Date')

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'batch.list'),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class manual_storage(models.Model):
    _name = 'manual.storage'
    _description = 'manual.storage'

    code = fields.Char(string='Code', size=64, required=True, help='Code')
    name = fields.Char(string='Name', size=64, required=True, help='Name')
    batch_id = fields.Many2one('commodity.batch', string='Commodity Batch', help='Commodity Batch')
    commodity_id = fields.Many2one('commodity.info', string='Commodity', help='Commodity')
    warehouse_id = fields.Many2one('warehouse.info', string='Warehouse', help='Warehouse')
    unit_id = fields.Many2one('base.unit', string='Unit')
    fixed_code = fields.Float(string='Fixed Code', digits=(16, 0), required=True, help='Fixed Code')
    number = fields.Float(string='Num', digits=(16, 0), help='Number')
    messages = fields.Char(string='Messages', help='Messages')
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help='Date')

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
        fixed_code = self.fixed_code
        num = int(self.number)
        rk_obj_id = self.env['warehouse.doc'].create(values)
        company_objs = self.env['company.info'].search([])
        if company_objs:
            for company_obj in company_objs:
                company_code = company_obj.company_code
        if rk_obj_id:
            i = 0
            for j in range(0, num):
                i = i + 1
                code = get_code(self, company_code, fixed_code, num, i)
                values = {
                    'code': code,
                    'name': code,
                    'line_id': str(rk_obj_id.id),
                    'number': 0,
                    'messages': ' ',
                }
                self.env['batch.list'].create(values)
        return {'type': 'ir.actions.act_window_close'}

    _defaults = {
        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'manual.storage'),
        'number': 1,
        'to_batch': 0,
        'from_batch': 0,
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
def get_code(self, get_kh, get_gd, get_num,get_i):
    kh = str(get_kh)
    gd = int(get_gd)
    num = int(get_num)
    i = int(get_i)
    str_bs = '000000000000000000'
    str_num = '100000000000000000000'
    ws = gd/2 - 1
    min_str = str_num[:ws]
    max_str = str_num[:ws+1]
    min_num = int(min_str) + num
    max_num = int(max_str) - 1
    all_the_text = ''
    #随机取两位数
    one = random.randint(10, 99)
    #被10除求商和玉树
    int_one = one // 10
    int_two = one % 10
    sj = random.randint(min_num, max_num)
    str1 = str(sj)
    code = (str_bs+str(i))
    cd = 0-(ws - len(str(kh)))
    str2 = str(kh)+code[cd:]
    str3 = ''
    for j in range(0, gd/2-1):
        if int_one % 2 == 0:
            str3 = str3 + str1[j] + str2[j]
        else:
            str3 = str3 + str2[j] + str1[j]
    int_end = int_two - gd + 2
    str3 = str3[int_end:] + str3[:int_two]
    str4 = str(one) + str3
    all_the_text = all_the_text + str4
    return all_the_text
    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: