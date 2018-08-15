# -*- coding: utf-8 -*-
from openerp import http, fields
import authorizer
import rest
import datetime
# import timedelta
import random
import jiemi

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
date_ref = datetime.datetime.now().strftime('%Y-%m-%d')
# _logger = logging.getLogger(__name__)

class OrderController(http.Controller):
    #扫码入库
    @authorizer.authorize
    @http.route('/api/kcgl/get_kcrk/<unit_id>', type='http', auth='none', methods=['GET'])
    def get_kcrk(self, unit_id, goods_id, batch_id, code_lists):
        #print code_lists
        rk_code = ''
        unit_obj = self.current_env['convert.info']
        unit_one_obj = unit_obj.search([('one_unit', '=', int(unit_id))])
        if not unit_one_obj:
            messages = u'请先维护计量单位换算！'
            return rest.render_json({'status': 'no', "message": messages, "data": messages})
        num_one = unit_one_obj.convert
        unit_two_obj = unit_obj.search([('one_unit', '=', int(unit_one_obj.two_unit.id))])
        if unit_two_obj:
            num_two = unit_two_obj.convert
        code = 'RKD' + date_ref[:4] + date_ref[5:7] + str(random.randint(100, 999))
        rkd_obj = self.current_env['warehouse.doc']
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
                ewm_code = str(batch_list['name'])
                batch_code = str(jiemi.def_jiemi(ewm_code))
            except:
                messages = u'非法条码，不能进行扫码入库，请联系管理员！'
                return rest.render_json({'status': 'no', "message": messages, "data": messages})
            #判断code的9-12位置是否000，如果为000 ，需要存储托盘
            # print type(batch_code)
            if batch_code[15:18] == '000':
                warehouse_one_obj = self.current_env['warehouse.one']
                batch_obj = warehouse_one_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', 'in')])
                if batch_obj:
                    rk_code = rk_code + ',' + ewm_code
                    continue
                # warehouse_one_obj = self.current_env['warehouse.one']
                #插入托盘表
                values = {
                    'code': str(ewm_code),
                    'name': str(batch_code),
                    'type': 'in',
                    'start_code': batch_code,
                    'end_code': batch_code,
                    'line_id': str(rkd_obj_id.id),
                    'number': 1,
                }
                warehouse_one_obj_id = warehouse_one_obj.create(values)
                bs_code = '000'+str(int(num_one))
                bs_code = bs_code[-3:]
                start_code = batch_code[:15] + '001' + batch_code[18:]
                end_code = batch_code[:15] + bs_code + batch_code[18:]
                values = {
                    'code': str(ewm_code),
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
                batch_obj = warehouse_two_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', 'in')])
                if not batch_obj:
                    warehouse_two_obj_id = warehouse_two_obj.create(values)
                #插入瓶
                bs_code = '000'+str(int(num_one))
                start_code = start_code
                end_code = batch_code[:15] + bs_code[-3:] + str('00'+str(int(num_two)))[-2:]
                values = {
                    'code': str(ewm_code),
                    'name': str(batch_code),
                    'type': 'in',
                    'start_code': start_code,
                    'end_code': end_code,
                    'line_id': str(rkd_obj_id.id),
                    'warehouse_two_id': warehouse_two_obj_id.id,
                    'number': str(num_one*num_two),
                    }
                batch_list_obj = self.current_env['warehouse.line']
                batch_list_obj.create(values)
                rkd_obj_id.update({'number': int(rkd_obj_id.number) + num_one*num_two})
            elif batch_code[15:18] != '000' and batch_code[-2:] == '00':
                warehouse_obj = self.current_env['warehouse.two']
                batch_obj = warehouse_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', 'in')])
                if batch_obj:
                    rk_code = rk_code + ',' + ewm_code
                    continue
                bs_code = '000'+str(num+int(batch_code[15:18]) - 1)
                bs_code = bs_code[-3:]
                start_code = batch_code
                end_code = batch_code[:15] + bs_code + batch_code[18:]
                values = {
                    'code': str(ewm_code),
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
                start_code = start_code
                end_code = batch_code[:18] + str('00'+str(int(num_one)))[-2:]
                values = {
                    'code': str(ewm_code),
                    'name': str(batch_code),
                    'type': 'in',
                    'start_code': start_code,
                    'end_code': end_code,
                    'line_id': str(rkd_obj_id.id),
                    'warehouse_two_id': warehouse_two_obj_id.id,
                    'number': str(num_one*num),
                    }
                batch_list_obj = self.current_env['warehouse.line']
                batch_list_obj.create(values)
                rkd_obj_id.update({'number': int(rkd_obj_id.number) + num_one*num})
            else:
                warehouse_obj = self.current_env['warehouse.line']
                batch_obj = warehouse_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', 'in')])
                if not batch_obj:
                    j = int(batch_code[-2:]) + int(num) - 1
                    bs_code = '00'+str(j)
                    values = {
                            'code': str(ewm_code),
                            'name': str(batch_code),
                            'type': 'in',
                            'start_code': batch_code,
                            'end_code': batch_code[:-2] + bs_code[-2:],
                            'line_id': str(rkd_obj_id.id),
                            'number': 1,
                            }
                    warehouse_obj.create(values)
                    rkd_obj_id.update({'number': int(rkd_obj_id.number) + int(num)})
        if len(rk_code) > 1:
            rk_code = rk_code[1:]
            messages = u'入库完成，请检查条码号为' + rk_code + u'的条码已入库!'
        else:
            messages = u'入库完成!'
        return rest.render_json({"status": "yes", "message": messages, "data": code_lists})
    #删除扫码入库
    @authorizer.authorize
    @http.route('/api/kcgl/del_kcrk/<code>', type='http', auth='none', methods=['GET'])
    def del_kcrk(self, code):
        warehouse_obj = self.current_env['warehouse.line'].search([('code', '=', code)])
        if not warehouse_obj:
            messages = u'该条码没有入库，不用删除，请直接入库！'
            return rest.render_json({"status": "no", "message": code, "data": messages})
        strsql = "delete from warehouse_line where code = '%s'; delete from warehouse_one where code = '%s'; delete from warehouse_two where code = '%s'" % (code, code, code)
        print strsql
        self.current_env.cr.execute(strsql)
        messages = u'已经删除！'
        return rest.render_json({"status": "yes", "message": code, "data": messages})
        # self.current_env.cr.execute('delete from ckgl_dddy;delete from dddy_line')
    #扫码出库
    @authorizer.authorize
    @http.route('/api/kcgl/get_kcck/<unit_id>', type='http', auth='none', methods=['GET'])
    def get_kcck(self, unit_id, goods_id, batch_id, agent_id, express_id, express_code,code_lists):
        code = 'CKD' + date_ref[:4] + date_ref[5:7] + str(random.randint(100, 999))
        rkd_obj = self.current_env['warehouse.doc']
        rk_code = ''
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
                ewm_code = str(batch_list['name'])
                batch_code = str(jiemi.def_jiemi(ewm_code))
            except:
                messages = u'非法条码，不能进行扫码出库，请联系管理员！'
                return rest.render_json({'status': 'no', "message": messages, "data": messages})
            #判断code的9-12位置是否000，如果为000 ，需要存储托盘
            # print type(batch_code)
            if batch_code[15:18] == '000':
                warehouse_one_obj = self.current_env['warehouse.one']
                batch_obj = warehouse_one_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', 'out')])
                if batch_obj:
                    rk_code = rk_code + ',' + ewm_code
                    continue
                # warehouse_one_obj = self.current_env['warehouse.one']
                unit_obj = self.current_env['convert.info']
                unit_one_obj = unit_obj.search([('one_unit', '=', int(unit_id))])
                if not unit_one_obj:
                    messages = u'请先维护计量单位换算！'
                    return rest.render_json({'status': 'no', "message": messages, "data": messages})
                num_one = unit_one_obj.convert
                unit_two_obj = unit_obj.search([('one_unit', '=', int(unit_one_obj.two_unit.id))])
                num_two = unit_two_obj.convert
                #插入托盘表
                values = {
                    'code': str(ewm_code),
                    'name': str(batch_code),
                    'type': 'out',
                    'start_code': batch_code,
                    'end_code': batch_code,
                    'line_id': str(rkd_obj_id.id),
                    'number': 1,
                }
                warehouse_one_obj_id = warehouse_one_obj.create(values)
                bs_code = '000'+str(int(num_one))
                bs_code =bs_code[-3:]
                start_code = batch_code[:15] + '001' + batch_code[18:]
                end_code = batch_code[:15] + bs_code + batch_code[18:]
                values = {
                    'code': str(ewm_code),
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
                batch_obj = warehouse_two_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', 'out')])
                if not batch_obj:
                    # warehouse_two_obj.create(values)
                    warehouse_two_obj_id = warehouse_two_obj.create(values)
                #插入箱号
                bs_code = '000'+str(int(num_one))
                start_code = start_code
                end_code = batch_code[:15] + bs_code[-3:] + str('00'+str(int(num_two)))[-2:]
                values = {
                    'code': str(ewm_code),
                    'name': str(batch_code),
                    'type': 'out',
                    'start_code': start_code,
                    'end_code': end_code,
                    'line_id': str(rkd_obj_id.id),
                    'warehouse_two_id': warehouse_two_obj_id.id,
                    'number': str(num_one*num_two),
                    }
                batch_list_obj = self.current_env['warehouse.line']
                batch_list_obj.create(values)
                rkd_obj_id.update({'number': int(rkd_obj_id.number) + num_one*num_two})
            elif batch_code[15:18] != '000' and batch_code[-2:] == '00':
                warehouse_obj = self.current_env['warehouse.two']
                batch_obj = warehouse_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', 'out')])
                if batch_obj:
                    rk_code = rk_code + ',' + ewm_code
                    continue
                unit_obj = self.current_env['convert.info']
                unit_one_obj = unit_obj.search([('one_unit', '=', int(unit_id))])
                if not unit_one_obj:
                    messages = u'请先维护计量单位换算！'
                    return rest.render_json({'status': 'no', "message": messages, "data": messages})
                num_one = unit_one_obj.convert
                bs_code = '000'+str(num+int(batch_code[15:18]) - 1)
                bs_code = bs_code[-3:]
                start_code = batch_code
                end_code = batch_code[:15] + bs_code + batch_code[18:]
                values = {
                    'code': str(ewm_code),
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
                # #插入箱号
                start_code = start_code
                end_code = batch_code[:18] + str('00'+str(int(num_one)))[-2:]
                values = {
                    'code': str(ewm_code),
                    'name': str(batch_code),
                    'type': 'out',
                    'start_code': start_code,
                    'end_code': end_code,
                    'line_id': str(rkd_obj_id.id),
                    'warehouse_two_id': warehouse_two_obj_id.id,
                    'number': str(num_one*num),
                    }
                batch_list_obj = self.current_env['warehouse.line']
                batch_list_obj.create(values)
                rkd_obj_id.update({'number': int(rkd_obj_id.number) + num_one*num})
            else:
                warehouse_obj = self.current_env['warehouse.line']
                batch_obj = warehouse_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', 'out')])
                if not batch_obj:
                    j = int(batch_code[-2:]) + int(num) - 1
                    bs_code = '00'+str(j)
                    values = {
                            'code': str(ewm_code),
                            'name': str(batch_code),
                            'type': 'out',
                            'start_code': batch_code,
                            'end_code': batch_code[:-2] + ('000' + bs_code[-2:] + number - 1)[-2:],
                            'line_id': str(rkd_obj_id.id),
                            'number': num,
                            }
                    warehouse_obj.create(values)
                    rkd_obj_id.update({'number': int(rkd_obj_id.number) + int(num)})
        if len(rk_code) > 1:
            rk_code = rk_code[1:]
            messages = u'出库完成，请检查条码号为' + rk_code + u'的条码已出库！'
        else:
            messages = u'出库完成!'
        return rest.render_json({"status": "yes", "message": messages, "data": code_lists})

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
                if code[:3] != '149':
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
        if code[15:18] == '000' and code[3:9] != u'012345':
            warehouse_line_obj = self.current_env['warehouse.one'].search([('type', '=', 'in'), ('start_code', '<=', code), ('end_code', '>=', code)])
        elif code[15:18] != '000' and code[-2:] == '00' and code[3:9] != u'012345':
            warehouse_line_obj = self.current_env['warehouse.two'].search([('type', '=', 'in'), ('start_code', '<=', code), ('end_code', '>=', code)])
        else:
            warehouse_line_obj = self.current_env['warehouse.line'].search([('type', '=', 'in'), ('start_code', '<=', code), ('end_code', '>=', code)])
        if warehouse_line_obj:
            batch_list_obj = self.current_env['batch.list'].search([('code', '=', code)])
            now = datetime.datetime.now()
            if not batch_list_obj:
                # date_hours = now + datetime.timedelta(hours=8)
                date_time = now.strftime('%Y-%m-%d %H:%M:%S')
                values = {
                    'code': code,
                    'name': code,
                    'number': 1,
                    'first_date': date_time,
                    'new_date': date_time,
                }
                batch_list_obj.create(values)
                messages = messages_one
            else:
                messages = messages_two
                number = int(batch_list_obj.number)
                messages = messages.replace('code', str(ewm_code))
                messages = messages.replace('d', str(batch_list_obj.first_date))
                if (now-datetime.datetime.strptime(str(batch_list_obj.new_date)[:19], '%Y-%m-%d %H:%M:%S')).seconds > 120:
                    batch_list_obj.update({'number': batch_list_obj.number + 1, 'new_date': now})
                    number = number + 1
                if number == 1:
                    messages = messages_one
                else:
                    messages = messages.replace('n', str(number))
        else:
            messages = u'你查询的是本公司产品数码，但是没有发生出入库！'
        return rest.render_json({"status": "yes", "message": ewm_code, "data": messages})