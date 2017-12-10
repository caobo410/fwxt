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
from openerp.osv import osv
import random
import jiemi
import storage
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
    line_id = fields.One2many('warehouse.line', 'line_id', string='瓶', copy=True)
    one_id = fields.One2many('warehouse.one', 'line_id', string='托', copy=True)
    two_id = fields.One2many('warehouse.two', 'line_id', string='箱', copy=True)
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
        # 'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'warehouse.line'),
        'date_confirm': lambda self, cr, uid, context={}: context.get('date', time.strftime("%Y-%m-%d")),
        'user_id': lambda cr, uid, id, c={}: id,
        'type': lambda obj, cr, uid, context: context['type'],
    }

class warehouse_one(models.Model):
    _name = 'warehouse.one'
    _description = 'warehouse.one'

    code = fields.Char(string='编号', size=64, help='编号')
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
        # 'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'warehouse.one'),
        'type': lambda obj, cr, uid, context: context['type'],
    }
class warehouse_two(models.Model):
    _name = 'warehouse.two'
    _description = 'warehouse.two'

    code = fields.Char(string='编号', size=64, help='编号')
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
        # 'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'warehouse.two'),
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
    state_code = fields.Char(string='起始号', required=True, help='起始号')
    batch_id = fields.Many2one('commodity.batch', string='商品批次', help='商品批次')
    commodity_id = fields.Many2one('commodity.info', string='商品', help='商品')
    warehouse_id = fields.Many2one('warehouse.info', string='仓库', help='仓库')
    unit_id = fields.Many2one('base.unit', string='单位')
    type = fields.Selection([('in', '入库'),
                             ('out', '出库')], '类型', required=True, help='类型')
    agent_id = fields.Many2one('agent.info', string='经销商', help='经销商')
    express_id = fields.Many2one('express.info', string='快递', help='快递')
    express_code = fields.Char(string='快递号', help='快递号')
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
        type = self.type
        if type == u'in':
            values = {
                'code': self.code,
                'name': self.name,
                'type': type,
                'batch_id': int(self.batch_id.id),
                'commodity_id': int(self.commodity_id.id),
                'warehouse_id': int(self.warehouse_id.id),
                'unit_id': int(self.unit_id.id),
                'number': str(self.number),
                'messages': u'手动入库',
            }
        else:
            values = {
                'code': self.code,
                'name': self.name,
                'type': type,
                'batch_id': int(self.batch_id.id),
                'agent_id': int(self.agent_id.id),
                'express_id': int(self.express_id.id),
                'express_code': str(self.express_code),
                'commodity_id': int(self.commodity_id.id),
                'unit_id': int(self.unit_id.id),
                'number': str(self.number),
                'messages': u'手动出库',
            }
        rk_code = ''
        code = self.code
        rkd_obj = self.env['warehouse.doc']
        rkd_list_obj = self.env['warehouse.line']
        rkd_list_obj = rkd_list_obj.search(
            [('code', '=', str(self.state_code)), ('type', '=', type)])
        if rkd_list_obj:
            raise osv.except_osv(('Error!'), ("Error!"))
            return False
        # rkd_obj_id = rkd_obj.create(values)
        try:
            xztm_code = jiemi.def_jiemi(str(self.state_code))
        except:
            # messages = u'非法条码，不能进行扫码入库，请联系管理员！'
            raise osv.except_osv(('Error!'), ("Error!"))
            return False
        if xztm_code == u'0000':
            raise osv.except_osv(('Error!'), ("Error!"))
            return False
        rkd_obj_id = rkd_obj.create(values)
        batch_code = str(xztm_code)
        if batch_code[3:9] == u'012345':
            start_int = int(batch_code[9:])
            start_code = batch_code[:9] + (u'000000000000000' + str(start_int))[-11:]
            end_code = batch_code[:9] + (u'00000000000000' + str(start_int + int(self.number) - 1))[-11:]
            values = {
                'code': str(self.state_code),
                'name': str(batch_code),
                'type': type,
                'start_code': start_code,
                'end_code': end_code,
                'line_id': str(rkd_obj_id.id),
                'warehouse_two_id': 0,
                'number': int(self.number),
            }
            batch_list_obj = self.env['warehouse.line']
            batch_obj = batch_list_obj.search(
                [('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', type)])
            if not batch_obj:
                batch_list_obj.create(values)
                return {'type': 'ir.actions.act_window_close'}
            raise osv.except_osv((u'数据错误!'), (u"该起始数据已经入库请检查!"))
            return False
        # for number in range(1, int(self.number)+1):
        number = int(self.number)
        # 判断code的9-12位置是否000，如果为000 ，需要存储托盘
        # print type(batch_code)
        if batch_code[15:18] == u'000':
            warehouse_one_obj = self.env['warehouse.one']
            batch_obj = warehouse_one_obj.search(
                [('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', type)])
            if batch_obj:
                # messages = u'改条码已经入库！'
                raise osv.except_osv(('Error!'), (u'改条码已经入库！'))
                return False
            # warehouse_one_obj = self.env['warehouse.one']
            unit_obj = self.env['convert.info']
            unit_one_obj = unit_obj.search([('one_unit', '=', int(self.unit_id))])
            if not unit_one_obj:
                # messages = u'请先维护计量单位换算！'
                raise osv.except_osv(('Error!'), (u'请先维护计量单位换算！'))
                return False
            num_one = unit_one_obj.convert
            unit_two_obj = unit_obj.search([('one_unit', '=', int(unit_one_obj.two_unit.id))])
            num_two = unit_two_obj.convert
            # 插入托盘表
            end_code = batch_code[:9] + (u'0000000' + str(int(batch_code[9:15]) + number - 1))[-6:] + batch_code[-5:]
            values = {
                'code': str(self.state_code),
                'name': str(batch_code),
                'type': type,
                'start_code': batch_code,
                'end_code': end_code,
                'line_id': str(rkd_obj_id.id),
                'number': int(self.number),
            }
            warehouse_one_obj_id = warehouse_one_obj.create(values)
            for number in range(1, int(self.number) + 1):
                tp_code = batch_code[:9] + (u'0000000' + str(int(batch_code[9:15]) + number - 1))[-6:] + batch_code[-5:]
                bs_code = '000' + str(int(num_one))
                bs_code = bs_code[-3:]
                start_code = tp_code[:15] + u'001' + tp_code[18:]
                end_code = tp_code[:15] + bs_code + tp_code[18:]
                values = {
                    'code': str(self.state_code),
                    'name': str(tp_code),
                    'type': type,
                    'start_code': start_code,
                    'end_code': end_code,
                    'line_id': str(rkd_obj_id.id),
                    'warehouse_one_id': warehouse_one_obj_id.id,
                    'number': num_one,
                }
                # 插入箱表
                warehouse_two_obj = self.env['warehouse.two']
                batch_obj = warehouse_two_obj.search(
                    [('start_code', '<=', tp_code), ('end_code', '>=', tp_code), ('type', '=', type)])
                if not batch_obj:
                    warehouse_two_obj_id = warehouse_two_obj.create(values)
                # 插入箱号
                for i in range(1, int(num_one) + 1):
                    bs_code = '000' + str(i)
                    bs_code = bs_code[-3:]
                    end_str = '000' + str(int(num_two))
                    xh_code = tp_code[:15] + bs_code + tp_code[18:-2] + u'00'
                    start_code = tp_code[:15] + bs_code + tp_code[18:-2] + u'01'
                    end_code = tp_code[:15] + bs_code + tp_code[18:-2] + end_str[-2:]
                    values = {
                        'code': str(self.state_code),
                        'name': str(xh_code),
                        'type': type,
                        'start_code': start_code,
                        'end_code': end_code,
                        'line_id': str(rkd_obj_id.id),
                        'warehouse_two_id': warehouse_two_obj_id.id,
                        'number': num_two,
                    }
                    batch_list_obj = self.env['warehouse.line']
                    batch_obj = batch_list_obj.search(
                        [('start_code', '<=', start_code), ('end_code', '>=', start_code), ('type', '=', type)])
                    if not batch_obj:
                        batch_list_obj.create(values)
                        rkd_obj_id.update({'number': int(rkd_obj_id.number) + num_two})
        elif batch_code[15:18] != '000' and batch_code[-2:] == '00':
            warehouse_obj = self.env['warehouse.two']
            batch_obj = warehouse_obj.search(
                [('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', type)])
            if batch_obj:
                # messages = u'改条码已经入库！'
                raise osv.except_osv(('Error!'), (u'改条码已经入库！'))
                return False
            unit_obj = self.env['convert.info']
            unit_one_obj = unit_obj.search([('one_unit', '=', int(self.unit_id))])
            if not unit_one_obj:
                # messages = u'请先维护计量单位换算！'
                raise osv.except_osv(('Error!'), (u'请先维护计量单位换算！'))
                return False
            num_one = unit_one_obj.convert
            bs_code = '000' + str(number + int(batch_code[15:18]) - 1)
            bs_code = bs_code[-3:]
            start_code = batch_code
            end_code = batch_code[:15] + bs_code + batch_code[18:]
            values = {
                'code': str(self.state_code),
                'name': str(batch_code),
                'type': type,
                'start_code': start_code,
                'end_code': end_code,
                'line_id': str(rkd_obj_id.id),
                'number': number,
            }
            # 插入箱表
            warehouse_two_obj = self.env['warehouse.two']
            warehouse_two_obj_id = warehouse_two_obj.create(values)
            # 插入箱号
            for i in range(1, int(number) + 1):
                j = i + int(batch_code[15:18]) - 1
                bs_code = '000' + str(j)
                bs_code = bs_code[-3:]
                end_str = '000' + str(int(num_one))
                xh_code = batch_code[:15] + bs_code + batch_code[18:-2] + '00'
                start_code = batch_code[:15] + bs_code + batch_code[18:-2] + '01'
                end_code = batch_code[:15] + bs_code + batch_code[18:-2] + end_str[-2:]
                values = {
                    'code': str(self.state_code),
                    'name': str(xh_code),
                    'type': type,
                    'start_code': start_code,
                    'end_code': end_code,
                    'line_id': str(rkd_obj_id.id),
                    'warehouse_two_id': warehouse_two_obj_id.id,
                    'number': num_one,
                }
                batch_list_obj = self.env['warehouse.line']
                batch_obj = batch_list_obj.search(
                    [('start_code', '<=', start_code), ('end_code', '>=', start_code), ('type', '=', type)])
                if not batch_obj:
                    batch_list_obj.create(values)
                    rkd_obj_id.update({'number': int(rkd_obj_id.number) + num_one})
        else:
            warehouse_obj = self.env['warehouse.line']
            batch_obj = warehouse_obj.search(
                [('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', type)])
            if not batch_obj:
                j = int(batch_code[-2:]) + int(number) - 1
                bs_code = '00' + str(j)
                values = {
                    'code': str(self.state_code),
                    'name': str(batch_code),
                    'type': type,
                    'start_code': batch_code,
                    'end_code': batch_code[:-2] + ('000' + bs_code[-2:] + number - 1)[-2:],
                    'line_id': str(rkd_obj_id.id),
                    'number': number,
                }
                warehouse_obj.create(values)
                rkd_obj_id.update({'number': int(rkd_obj_id.number) + int(number)})
        if len(rk_code) > 1:
            rk_code = rk_code[1:]
            if type == 'in':
                messages = u'入库完成，请检查条码号为' + rk_code + u'的条码已入库!'
            else:
                messages = u'出库完成，请检查条码号为' + rk_code + u'的条码是否出库!'
        else:
            if type == 'in':
                messages = u'入库完成!'
            else:
                messages = u'出库完成!'
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