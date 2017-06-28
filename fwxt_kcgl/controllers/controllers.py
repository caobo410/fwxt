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
        # print code_lists
        code = 'RKD' + date_ref[:4] + date_ref[5:7] + str(random.randint(100, 999))
        rkd_obj = self.current_env['warehouse.doc']
        company_objs = self.current_env['company.info'].search([])
        kh = ''
        # print '123'
        for company_obj in company_objs:
            kh = company_obj.company_code
        values = []
        values = {
            'code': code,
            'name': code,
            'type': 'in',
            'batch_id': int(batch_id),
            'commodity_id': int(goods_id),
            'unit_id': int(unit_id),
        }
        # print values
        rkd_obj_id = rkd_obj.create(values)
        warehouse_obj = self.current_env['warehouse.line']
        batch_lists = eval(code_lists)
        j = 0
        for batch_list in batch_lists:
            start_code = ''
            end_code = ''
            num = int(batch_list['number'])
            try:
                # print batch_list['name']
                batch_code = str(batch_list['name'])
                start_code = str(jiemi.def_jiemi(batch_code))
                end_code = str(int(start_code)-1 + num)
                # end_code = end_code[0-len(start_code):]
            except:
                messages = u'非法条码，不能进行扫码入库，请联系管理员！'
                return rest.render_json({'status': 'no', "message": messages, "data": messages})
            values = {
                'code': str(batch_code),
                'name': str(batch_code),
                'type': 'in',
                'start_code': start_code,
                'end_code': end_code,
                'line_id': str(rkd_obj_id.id),
                'number': num,
            }
            batch_obj = warehouse_obj.search([('start_code', '<=', start_code), ('end_code', '>=', start_code)])
            if batch_obj:
                messages = u'该条码已经入库过，请检查入库单号为' + batch_obj.line_id.code + u'的单据!'
                # print messages
                return rest.render_json({'status': 'no', "message": messages, "data": messages})
            else:
                # print values
                warehouse_obj.create(values)
                rkd_obj_id.update({'number': int(rkd_obj_id.number) + num})
        return rest.render_json({"status": "yes", "message": code, "data": code_lists})

    #扫码出库
    @authorizer.authorize
    @http.route('/api/kcgl/get_kcck/<unit_id>', type='http', auth='none', methods=['GET'])
    def get_kcck(self, unit_id, goods_id, batch_id, agent_id, express_id, express_code,code_lists):
        code = 'RKD' + date_ref[:4] + date_ref[5:7] + str(random.randint(100, 999))
        rkd_obj = self.current_env['warehouse.doc']
        values = []
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
        warehouse_obj = self.current_env['warehouse.line']
        batch_lists = eval(code_lists)
        j = 0
        for batch_list in batch_lists:
            start_code = ''
            end_code = ''
            num = int(batch_list['number'])
            try:
                batch_code = str(batch_list['name'])
                start_code = str(jiemi.def_jiemi(batch_code))
                end_code = str(int(start_code) - 1 + num)
                # print start_code,end_code
            except:
                messages = u'非法条码，不能进行扫码出库，请联系管理员！'
                return rest.render_json({'status': 'no', "message": messages, "data": messages})
            values = {
                'code': str(batch_code),
                'name': str(batch_code),
                'type': 'out',
                'start_code': start_code,
                'end_code': end_code,
                'line_id': str(rkd_obj_id.id),
                'number': num,
            }
            batch_obj = warehouse_obj.search([('type', '=', 'out'), ('start_code', '<=', start_code), ('end_code', '>=', start_code)])
            if batch_obj:
                messages = u'该条码已经出库过，请检查出库单号为' + batch_obj.line_id.code + u'的单据!'
                return rest.render_json({'status': 'no', "message": messages, "data": messages})
            else:
                warehouse_obj.create(values)
                rkd_obj_id.update({'number': rkd_obj_id.number + num})
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
                if len(ewm_code) != 23 and len(ewm_code) != 25:
                    messages = u'该产品不是本公司产品请联系公司'
                    return rest.render_json({'status': 'no', "message": ewm_code, "data": messages})
                # print tm_code
                code = jiemi.def_jiemi(ewm_code)
                # print '123'
            except:
                messages = u'该产品不是本公司产品请联系公司!'
                return rest.render_json({'status': 'no', "message": ewm_code, "data": messages})
            # company_objs = self.current_env['company.info'].search([])
            # if company_objs:
            #     for company_obj in company_objs:
            #         company_code = company_obj.company_code
            #     len_code = jiemi.def_company(ewm_code)
            #     if company_code != len_code:
            #         messages = u'该产品不是本公司产品，请联系公司！'
            #         return rest.render_json({'status': 'no', "message": ewm_code, "data": messages})
            # else:
            #     messages = u'请在公司简介中维护公司信息及公司编码！'
            #     return rest.render_json({"status": "yes", "message": ewm_code, "data": messages})
            other_objs = self.current_env['other.info'].search([])
            if other_objs:
                for other_obj in other_objs:
                    messages_one = other_obj.Search
                    messages_two = other_obj.search_two
            else:
                messages = u'请在其他信息中维护查询内容及二次查询内容！'
                return rest.render_json({"status": "no", "message": ewm_code, "data": messages})
        print code
        warehouse_line_obj = self.current_env['warehouse.line'].search([('type', '=', 'out'), ('start_code', '<=', code), ('end_code', '>=', code)])
        if warehouse_line_obj:
            batch_list_obj = self.current_env['batch.list'].search([('code', '=', code)])
            messages = ''
            if not batch_list_obj:
                values = []
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