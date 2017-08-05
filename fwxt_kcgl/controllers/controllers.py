# -*- coding: utf-8 -*-
from openerp import http, fields
import authorizer
import rest
from datetime import datetime
# import timedelta
import random
import jiemi

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


date_ref = datetime.now().strftime('%Y-%m-%d')
date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# _logger = logging.getLogger(__name__)

class OrderController(http.Controller):
    #扫码入库
    @authorizer.authorize
    @http.route('/api/kcgl/get_kcrk/<unit_id>', type='http', auth='none', methods=['GET'])
    def get_kcrk(self, unit_id, goods_id, batch_id, code_lists):
        #print code_lists
        code = 'RKD' + date_ref[:4] + date_ref[5:7] + str(random.randint(100, 999))
        rkd_obj = self.current_env['warehouse.doc']
        company_objs = self.current_env['company.info'].search([])
        values = {
            'code': code,
            'name': code,
            'type': 'in',
            'batch_id': int(batch_id),
            'commodity_id': int(goods_id),
            'unit_id': int(unit_id),
        }
        rkd_obj_id = rkd_obj.create(values)
        batch_lists = eval(code_lists)
        for batch_list in batch_lists:
            num = int(batch_list['number'])
            try:
                batch_code = str(batch_list['name'])
                batch_code = str(jiemi.def_jiemi(batch_code))
            except:
                messages = u'非法条码，不能进行扫码入库，请联系管理员！'
                return rest.render_json({'status': 'no', "message": messages, "data": messages})
            #判断code的9-12位置是否000，如果为000 ，需要存储托盘
            # print type(batch_code)
            if batch_code[9:12] == '000':
                warehouse_obj = self.current_env['warehouse.one']
                batch_obj = warehouse_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code)])
                if batch_obj:
                    messages = u'该条码已经入库过，请检查入库单号为' + batch_obj.line_id.code + u'的单据!'
                return rest.render_json({'status': 'no', "message": messages, "data": messages})
                warehouse_one_obj = self.current_env['warehouse.one']
                unit_obj = self.current_env['convert.info']
                unit_one_obj = unit_obj.search([('one_unit', '=', int(unit_id))])
                if not unit_one_obj:
                    messages = u'请先维护计量单位换算！'
                    return rest.render_json({'status': 'no', "message": messages, "data": messages})
                num_one = unit_one_obj.convert
                unit_two_obj = unit_obj.search([('two_unit', '=', int(unit_one_obj.one_unit.id))])
                num_two = unit_two_obj.convert
                end_code = '00000'+str(int(batch_code[12:-2])+int(num)-1)
                #插入托盘表
                values={
                    'name': str(batch_code),
                    'type': 'in',
                    'start_code': batch_code,
                    'end_code': batch_code,
                    'line_id': str(rkd_obj_id.id),
                    'number': 1,
                }
                warehouse_one_obj_id=warehouse_one_obj.create(values)
                bs_code = '000'+str(int(num_one))
                bs_code =bs_code[-3:]
                start_code = batch_code[:9] + '001' + batch_code[12:]
                end_code = batch_code[:9] + bs_code + batch_code[12:]
                values ={
                    'name': str(batch_code),
                    'type': 'in',
                    'start_code': start_code,
                    'end_code': end_code,
                    'line_id': str(rkd_obj_id.id),
                    'warehouse_one_id': warehouse_one_obj_id.id,
                    'number': num_one,
                }
                #插入箱表
                warehouse_two_obj = self.current_env['warehouse.two']
                warehouse_two_obj_id = warehouse_two_obj.create(values)
                #插入箱号
                for i in range(1, int(num_one)):
                    bs_code = '000'+str(i)
                    bs_code = bs_code[-3:]
                    end_str ='000'+str(int(num_two))
                    xh_code = batch_code[:9] + bs_code + batch_code[12:-2] + '00'
                    start_code = batch_code[:9] + bs_code + batch_code[12:-2] + '01'
                    end_code = batch_code[:9] + bs_code + batch_code[12:-2] + end_str[-2:]
                    values = {
                        'name': str(xh_code),
                        'type': 'in',
                        'start_code': start_code,
                        'end_code': end_code,
                        'line_id': str(rkd_obj_id.id),
                        'warehouse_two_id': warehouse_two_obj_id.id,
                        'number': num,
                        }
                    batch_list_obj = self.current_env['warehouse.line']
                    batch_list_obj.create(values)
                # print values
                rkd_obj_id.update({'number': int(rkd_obj_id.number) + 1})
            elif batch_code[9:12] != '000' and batch_code[-2:] == '00':
                warehouse_obj = self.current_env['warehouse.two']
                batch_obj = warehouse_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code)])
                if batch_obj:
                    messages = u'该条码已经入库过，请检查入库单号为' + batch_obj.line_id.code + u'的单据!'
                unit_obj = self.current_env['convert.info']
                unit_one_obj = unit_obj.search([('one_unit', '=', int(unit_id))])
                if not unit_one_obj:
                    messages = u'请先维护计量单位换算！'
                    return rest.render_json({'status': 'no', "message": messages, "data": messages})
                num_one = unit_one_obj.convert
                bs_code = '000'+str(num+int(batch_code[9:12]))
                bs_code = bs_code[-3:]
                start_code = batch_code
                end_code = batch_code[:9] + bs_code + batch_code[12:]
                #插入托盘表
                values={
                    'name': str(batch_code),
                    'type': 'in',
                    'start_code': start_code,
                    'end_code': end_code,
                    'line_id': str(rkd_obj_id.id),
                    'number': num,
                }
                #插入箱表
                warehouse_two_obj = self.current_env['warehouse.two']
                warehouse_two_obj_id = warehouse_two_obj.create(values)
                #插入箱号
                for i in range(1, int(num)):
                    j = i + int(batch_code[9:12]) - 1
                    bs_code = '000'+str(j)
                    bs_code = bs_code[-3:]
                    end_str ='000'+str(int(num_one))
                    xh_code = batch_code[:9] + bs_code + batch_code[12:-2] + '00'
                    start_code = batch_code[:9] + bs_code + batch_code[12:-2] + '01'
                    end_code = batch_code[:9] + bs_code + batch_code[12:-2] + end_str[-2:]
                    values = {
                        'code': str(xh_code),
                        'name': str(xh_code),
                        'type': 'in',
                        'start_code': start_code,
                        'end_code': end_code,
                        'line_id': str(rkd_obj_id.id),
                        'warehouse_two_id': warehouse_two_obj_id.id,
                        'number': num,
                        }
                    batch_list_obj = self.current_env['warehouse.line']
                    batch_list_obj.create(values)
                rkd_obj_id.update({'number': int(rkd_obj_id.number) + 1})
            else:
                for i in range(1, num):
                    warehouse_obj = self.current_env['warehouse.two']
                    batch_obj = warehouse_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code)])
                    if not batch_obj:
                        j = i + int(batch_code[-8:]) + int(num) - 1
                        bs_code = '00000000000'+str(j)
                        values = {
                                'code': str(batch_code),
                                'name': str(batch_code),
                                'type': 'in',
                                'start_code': batch_code,
                                'end_code': batch_code[:12] + bs_code[-8:],
                                'line_id': str(rkd_obj_id.id),
                                'number': 1,
                                }
                        batch_list_obj = self.current_env['warehouse.line']
                        batch_list_obj.create(values)
                        rkd_obj_id.update({'number': int(rkd_obj_id.number) + 1})
        return rest.render_json({"status": "yes", "message": code, "data": code_lists})
    #删除扫码入库
    @authorizer.authorize
    @http.route('/api/kcgl/del_kcrk/<code>', type='http', auth='none', methods=['GET'])
    def del_kcrk(self, code):
        if code[9:12] == '000':
            warehouse_obj = self.current_env['warehouse.one'].search([('name', '=', code)])
            str_one = code[:9]
            str_two = code[-8:]
            self.current_env.cr.execute("delete from warehouse_line where where SUBSTR(name,1,9)= '%s' and SUBSTR(name,13,20)='%s'; delete from warehouse_one where name = '%s'; delete from warehouse_two where name = '%s'" % (str_one, str_two, code, code))
        elif code[9:12] != '000' and batch_code[-2:] == '00':
            str_one = code[:9]
            str_two = code[-8:]
            warehouse_obj = self.current_env['warehouse.two'].search([('name', '=', code)])
            self.current_env.cr.execute("delete from warehouse_line where where SUBSTR(name,1,9)= '%s' and SUBSTR(name,13,20)='%s'; delete from warehouse_two where name = '%s'" % (str_one, str_two,  code))
        else:
            warehouse_obj = self.current_env['warehouse.line'].search([('code', '=', code)])
        if not warehouse_obj:
            messages = u'该条码没有入库，不用删除，请直接入库！'
            return rest.render_json({"status": "no", "message": code, "data": messages})
        self.current_env.cr.execute("delete from warehouse_line where name = '%s' " % code)
        messages = u'已经删除除！'
        return rest.render_json({"status": "yes", "message": code, "data": messages})
        # self.current_env.cr.execute('delete from ckgl_dddy;delete from dddy_line')
    #扫码出库
    @authorizer.authorize
    @http.route('/api/kcgl/get_kcck/<unit_id>', type='http', auth='none', methods=['GET'])
    def get_kcck(self, unit_id, goods_id, batch_id, agent_id, express_id, express_code,code_lists):
        code = 'CKD' + date_ref[:4] + date_ref[5:7] + str(random.randint(100, 999))
        rkd_obj = self.current_env['warehouse.doc']
        values = {
            'code': code,
            'name': code,
            'type': 'out',
            'batch_id': int(batch_id),
            'agent_id': int(agent_id),
            'express_id': int(express_id),
            'express_code': str(express_code),
            'commodity_id': int(goods_id),
            'unit_id': int(unit_id),
        }
        rkd_obj_id = rkd_obj.create(values)
        batch_lists = eval(code_lists)
        for batch_list in batch_lists:
            num = int(batch_list['number'])
            try:
                batch_code = str(batch_list['name'])
                batch_code = str(jiemi.def_jiemi(batch_code))
            except:
                messages = u'非法条码，不能进行扫码入库，请联系管理员！'
                return rest.render_json({'status': 'no', "message": messages, "data": messages})
            #判断code的9-12位置是否000，如果为000 ，需要存储托盘
            # print type(batch_code)
            if batch_code[9:12] == '000':
                warehouse_obj = self.current_env['warehouse.one']
                batch_obj = warehouse_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code)])
                if batch_obj:
                    messages = u'该条码已经入库过，请检查入库单号为' + batch_obj.line_id.code + u'的单据!'
                return rest.render_json({'status': 'no', "message": messages, "data": messages})
                warehouse_one_obj = self.current_env['warehouse.one']
                unit_obj = self.current_env['convert.info']
                unit_one_obj = unit_obj.search([('one_unit', '=', int(unit_id))])
                if not unit_one_obj:
                    messages = u'请先维护计量单位换算！'
                    return rest.render_json({'status': 'no', "message": messages, "data": messages})
                num_one = unit_one_obj.convert
                unit_two_obj = unit_obj.search([('two_unit', '=', int(unit_one_obj.one_unit.id))])
                num_two = unit_two_obj.convert
                #插入托盘表
                values={
                    'name': str(batch_code),
                    'type': 'out',
                    'start_code': batch_code,
                    'end_code': batch_code,
                    'line_id': str(rkd_obj_id.id),
                    'number': 1,
                }
                warehouse_one_obj_id = warehouse_one_obj.create(values)
                bs_code = '000'+str(int(num_one))
                bs_code = bs_code[-3:]
                start_code = batch_code[:9] + '001' + batch_code[12:]
                end_code = batch_code[:9] + bs_code + batch_code[12:]
                values = {
                    'name': str(batch_code),
                    'type': 'out',
                    'start_code': start_code,
                    'end_code': end_code,
                    'line_id': str(rkd_obj_id.id),
                    'warehouse_one_id': warehouse_one_obj_id.id,
                    'number': num_one,
                }
                #插入箱表
                warehouse_two_obj = self.current_env['warehouse.two']
                warehouse_two_obj_id = warehouse_two_obj.create(values)
                #插入箱号
                for i in range(1, int(num_one)):
                    bs_code = '000'+str(i)
                    bs_code = bs_code[-3:]
                    end_str = '000' + str(int(num_two))
                    xh_code = batch_code[:9] + bs_code + batch_code[12:-2] + '00'
                    start_code = batch_code[:9] + bs_code + batch_code[12:-2] + '01'
                    end_code = batch_code[:9] + bs_code + batch_code[12:-2] + end_str[-2:]
                    values = {
                        'name': str(xh_code),
                        'type': 'out',
                        'start_code': start_code,
                        'end_code': end_code,
                        'line_id': str(rkd_obj_id.id),
                        'warehouse_two_id': warehouse_two_obj_id.id,
                        'number': num,
                        }
                    batch_list_obj = self.current_env['warehouse.line']
                    batch_list_obj.create(values)
                # print values
                rkd_obj_id.update({'number': int(rkd_obj_id.number) + 1})
            elif batch_code[9:12] != '000' and batch_code[-2:] == '00':
                warehouse_obj = self.current_env['warehouse.two']
                batch_obj = warehouse_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code),('end_code', '>=', batch_code)])
                if batch_obj:
                    messages = u'该条码已经出库过，请检查出库单号为' + batch_obj.line_id.code + u'的单据!'
                unit_obj = self.current_env['convert.info']
                unit_one_obj = unit_obj.search([('one_unit', '=', int(unit_id))])
                if not unit_one_obj:
                    messages = u'请先维护计量单位换算！'
                    return rest.render_json({'status': 'no', "message": messages, "data": messages})
                num_one = unit_one_obj.convert
                bs_code = '000'+str(num+int(batch_code[9:12]))
                bs_code = bs_code[-3:]
                start_code = batch_code
                end_code = batch_code[:9] + bs_code + batch_code[12:]
                #插入托盘表
                values={
                    'name': str(batch_code),
                    'type': 'out',
                    'start_code': start_code,
                    'end_code': end_code,
                    'line_id': str(rkd_obj_id.id),
                    'number': num,
                }
                #插入箱表
                warehouse_two_obj = self.current_env['warehouse.two']
                warehouse_two_obj_id = warehouse_two_obj.create(values)
                #插入箱号
                for i in range(1, int(num)):
                    j = i + int(batch_code[9:12]) - 1
                    bs_code = '000'+str(j)
                    bs_code = bs_code[-3:]
                    end_str = '000' +str(int(num_one))
                    xh_code = batch_code[:9] + bs_code + batch_code[12:-2] + '00'
                    start_code = batch_code[:9] + bs_code + batch_code[12:-2] + '01'
                    end_code = batch_code[:9] + bs_code + batch_code[12:-2] + end_str[-2:]
                    values = {
                        'code': str(xh_code),
                        'name': str(xh_code),
                        'type': 'out',
                        'start_code': start_code,
                        'end_code': end_code,
                        'line_id': str(rkd_obj_id.id),
                        'warehouse_two_id': warehouse_two_obj_id.id,
                        'number': num,
                        }
                    batch_list_obj = self.current_env['warehouse.line']
                    batch_list_obj.create(values)
                rkd_obj_id.update({'number': int(rkd_obj_id.number) + 1})
            else:
                for i in range(1, num):
                    warehouse_obj = self.current_env['warehouse.two']
                    batch_obj = warehouse_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code)])
                    if not batch_obj:
                        j = i + int(batch_code[-8:]) + int(num) - 1
                        bs_code = '00000000000'+str(j)
                        values = {
                                'code': str(batch_code),
                                'name': str(batch_code),
                                'type': 'out',
                                'start_code': batch_code,
                                'end_code': batch_code[:12] + bs_code[-8:],
                                'line_id': str(rkd_obj_id.id),
                                'number': 1,
                                }
                        batch_list_obj = self.current_env['warehouse.line']
                        batch_list_obj.create(values)
                        rkd_obj_id.update({'number': int(rkd_obj_id.number) + 1})
        return rest.render_json({"status": "yes", "message": code, "data": code_lists})

    #查询
    @authorizer.authorize
    @http.route('/api/kcgl/get_search/<code>', type='http', auth='none', methods=['GET'])
    def get_search(self, code):
        messages_one = ''
        messages_two = ''
        ewm_code = str(code)
        if not ewm_code:
            messages = u'二维码损坏，无法正确获取到条码信息！'
            return rest.render_json({"status": "no", "message": ewm_code, "data": messages})
        else:
            try:
                if len(ewm_code) != 25:
                    messages = u'该产品不是本公司产品请联系公司'
                    return rest.render_json({'status': 'no', "message": ewm_code, "data": messages})
                code = jiemi.def_jiemi(ewm_code)
                if ewm_code[:3] == '149':
                    messages = u'该产品不是本公司产品请联系公司'
                    return rest.render_json({'status': 'no', "message": ewm_code, "data": messages})
            except:
                messages = u'该产品不是本公司产品请联系公司!'
                return rest.render_json({'status': 'no', "message": ewm_code, "data": messages})
            other_objs = self.current_env['other.info'].search([])
            if other_objs:
                for other_obj in other_objs:
                    messages_one = other_obj.Search
                    messages_two = other_obj.search_two
            else:
                messages = u'请在其他信息中维护查询内容及二次查询内容！'
                return rest.render_json({"status": "no", "message": ewm_code, "data": messages})
        # print code
        if batch_code[9:12] != '000':
            warehouse_line_obj = self.current_env['warehouse.one'].search([('type', '=', 'out'), ('start_code', '<=', code), ('end_code', '>=', code)])
        elif batch_code[9:12] != '000' and batch_code[-2:] == '00':
            warehouse_line_obj = self.current_env['warehouse.two'].search([('type', '=', 'out'), ('start_code', '<=', code), ('end_code', '>=', code)])
        else:
            warehouse_line_obj = self.current_env['warehouse.line'].search([('type', '=', 'out'), ('start_code', '<=', code), ('end_code', '>=', code)])
        if warehouse_line_obj:
            batch_list_obj = self.current_env['batch.list'].search([('code', '=', code)])
            if not batch_list_obj:
                values = {
                    'code': code,
                    'name': code,
                    'number': 1,
                    'first_date': date_time,
                }
                batch_list_obj.create(values)
                messages = messages_one
            else:
                messages = messages_two
                number = int(batch_list_obj.number + 1)
                messages = messages.replace('code', str(ewm_code))
                messages = messages.replace('n', str(number))
                messages = messages.replace('d', str(batch_list_obj.first_date))
                batch_list_obj.update({'number': batch_list_obj.number + 1})
        else:
            messages = u'你查询的是本公司产品数码，但是没有发生出入库！'
        return rest.render_json({"status": "yes", "message": ewm_code, "data": messages})