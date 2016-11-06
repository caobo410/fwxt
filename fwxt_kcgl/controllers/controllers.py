# -*- coding: utf-8 -*-
from openerp import http, fields
import authorizer
import rest
from datetime import datetime
import random

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


date_ref = datetime.now().strftime('%Y-%m-%d')
# _logger = logging.getLogger(__name__)

class OrderController(http.Controller):
    #商品批次信息
    @authorizer.authorize
    @http.route('/api/kcgl/get_batch_list/<code>', type='http', auth='none', methods=['GET'])
    def get_batch_list(self, code):
        commodity_obj = self.current_env['batch.list'].search([('name', '=', code)])
        if not commodity_obj:
            return rest.render_json({"status": "no", "message": code, "data": ''})
        commodity_list = {}
        commodity_list['code'] = commodity_obj.line_id.batch_id.code
        commodity_list['name'] = commodity_obj.line_id.batch_id.name
        commodity_list['batch'] = commodity_obj.line_id.batch_id.batch
        commodity_list['commodity'] = commodity_obj.line_id.commodity_id.name
        return rest.render_json({"status": "yes", "message": code, "data": commodity_list})
    #原材料批次信息
    @authorizer.authorize
    @http.route('/api/kcgl/get_material_batch/<code>', type='http', auth='none', methods=['GET'])
    def get_material_batch(self, code):
        commodity_obj = self.current_env['batch.list'].search([('name', '=', code)])
        if not commodity_obj:
            return rest.render_json({"status": "no", "message": code, "data": ''})
        batch_objs = commodity_obj.line_id.batch_id.material_batch_id
        batch_lists = []
        for batch_obj in batch_objs:
            batch_list = {}
            batch_list['code'] = batch_obj.code
            batch_list['name'] = batch_obj.name
            batch_list['batch'] = batch_obj.batch
            batch_list['materia'] = batch_obj.materia_id.name
            batch_list['supplier'] = batch_obj.supplier_id.name
            batch_lists.append(batch_list)
        return rest.render_json({"status": "yes", "message": code, "data": batch_lists})

    #加工过程
    @authorizer.authorize
    @http.route('/api/kcgl/get_commodity_making/<code>', type='http', auth='none', methods=['GET'])
    def get_commodity_making(self, code):
        commodity_obj = self.current_env['batch.list'].search([('name', '=', code)])
        if not commodity_obj:
            return rest.render_json({"status": "no", "message": code, "data": ''})
        commodity_id = commodity_obj.line_id.commodity_id.id
        making_obj = self.current_env['commodity.making'].search([('commodity_id', '=', commodity_id)])
        making_list_objs = making_obj.line_id
        if not making_list_objs:
            return rest.render_json({"status": "no", "message": code, "data": ''})
        making_lists = []
        for making_list_obj in making_list_objs:
            making_list = {}
            making_list['code'] = making_list_obj.code
            making_list['name'] = making_list_obj.name
            making_list['type'] = making_list_obj.type.name
            making_list['messages'] = making_list_obj.messages
            making_lists.append(making_list)
        return rest.render_json({"status": "yes", "message": code, "data": making_lists})

    #生产过程
    @authorizer.authorize
    @http.route('/api/kcgl/get_commodity_produce/<code>', type='http', auth='none', methods=['GET'])
    def get_commodity_produce(self, code):
        commodity_obj = self.current_env['batch.list'].search([('name', '=', code)])
        if not commodity_obj:
            return rest.render_json({"status": "no", "message": code, "data": ''})
        commodity_id = commodity_obj.line_id.commodity_id.id
        produce_obj = self.current_env['commodity.produce'].search([('commodity_id', '=', commodity_id)])
        produce_list_objs = produce_obj.line_id
        if not produce_list_objs:
            return rest.render_json({"status": "no", "message": code, "data": ''})
        produce_lists = []
        for produce_list_obj in produce_list_objs:
            produce_list = {}
            produce_list['code'] = produce_list_obj.code
            produce_list['name'] = produce_list_obj.name
            produce_list['type'] = produce_list_obj.type.name
            produce_list['messages'] = produce_list_obj.messages
            produce_lists.append(produce_list)
        return rest.render_json({"status": "yes", "message": code, "data": produce_lists})

    #质检公司
    @authorizer.authorize
    @http.route('/api/kcgl/get_commodity_check/<code>', type='http', auth='none', methods=['GET'])
    def get_commodity_check(self, code):
        commodity_obj = self.current_env['batch.list'].search([('name', '=', code)])
        if not commodity_obj:
            return rest.render_json({"status": "no", "message": code, "data": ''})
        commodity_id = commodity_obj.line_id.commodity_id.id
        check_obj = self.current_env['commodity.check'].search([('commodity_id', '=', commodity_id)])
        check_list_objs = check_obj.line_id
        if not check_list_objs:
            return rest.render_json({"status": "no", "message": code, "data": ''})
        check_lists = []
        for check_list_obj in check_list_objs:
            check_list = {}
            check_list['code'] = check_list_obj.code
            check_list['name'] = check_list_obj.name
            check_list['comany'] = check_list_obj.check_id.name
            check_list['type'] = check_list_obj.type.name
            check_list['messages'] = check_list_obj.messages
            check_lists.append(check_list)
        return rest.render_json({"status": "yes", "message": code, "data": check_lists})
    #扫码入库
    @authorizer.authorize
    @http.route('/api/kcgl/get_kcrk/<unit_id>', type='http', auth='none', methods=['GET'])
    def get_kcrk(self, unit_id, goods_id, batch_id, code_lists):
        code = 'RKD' + date_ref[:4] + date_ref[5:7] + str(random.randint(100, 999))
        rkd_obj = self.current_env['warehouse.doc']
        values = []
        values = {
            'code': code,
            'name': code,
            'type': 'in',
            'batch_id': int(batch_id),
            'commodity_id': int(goods_id),
            'unit_id': int(unit_id),
        }
        rkd_obj_id = rkd_obj.create(values)
        list_obj = self.current_env['batch.list']
        batch_lists = eval(code_lists)
        j = 1
        for batch_list in batch_lists:
            num = int(batch_list[1])
            code = int(batch_list[0])-1
            for n in  range(1, num):
                values = {
                    'code': str(code+n),
                    'name': str(code+n),
                    'line_id': str(rkd_obj_id.id),
                }
                list_obj.create(values)
                j = j + 1
        rkd_obj_id.update({'number': j})
        return rest.render_json({"status": "yes", "message": code, "data": code_lists})
    #扫码出库
    @authorizer.authorize
    @http.route('/api/kcgl/get_kcck/<unit_id>', type='http', auth='none', methods=['GET'])
    def get_kcck(self, unit_id, goods_id, batch_id, agent_id, express_id,code_lists):
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
            'commodity_id': int(goods_id),
            'unit_id': int(unit_id),
        }
        rkd_obj_id = rkd_obj.create(values)
        list_obj = self.current_env['batch.list']
        batch_lists = eval(code_lists)
        j = 0
        for batch_list in batch_lists:
            num = int(batch_list[1])
            code = int(batch_list[0])-1
            for n in range(1, num):
                values = {
                    'code': str(code+n),
                    'name': str(code+n),
                    'line_id': str(rkd_obj_id.id),
                }
                list_obj.create(values)
                j = j + 1
        rkd_obj_id.update({'number': j})
        return rest.render_json({"status": "yes", "message": code, "data": code_lists})
