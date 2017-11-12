# -*- coding: utf-8 -*-
from openerp import http
from openerp import http, fields
import authorizer
import rest
from datetime import datetime
import jiemi
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


date_ref = datetime.now().strftime('%Y-%m-%d')
# _logger = logging.getLogger(__name__)

class OrderController(http.Controller):
    # 获取批次
    #http://localhost:8069/api/jcsj/get_batch/batch
    @authorizer.authorize
    @http.route('/api/batch/get_commodity_batch/<batch>', type='http', auth='none', methods=['GET'])
    def get_commodity_batch(self, batch):
        batch_objs = self.current_env['commodity.batch'].search([])
        if not batch_objs:
            return rest.render_json({"status": "no", "message": "", "data": ''})
        batch_lists = []
        for batch_obj in batch_objs:
            batch_list = {}
            batch_list['id'] = batch_obj.id
            batch_list['code'] = batch_obj.code
            batch_list['name'] = batch_obj.batch
            batch_lists.append(batch_list)
        return rest.render_json({"status": "yes", "message": "", "data": batch_lists})
    # 获取批次
    #http://localhost:8069/api/jcsj/get_batch/batch
    @authorizer.authorize
    @http.route('/api/batch/get_commodity_batch_search/<batch>', type='http', auth='none', methods=['GET'])
    def get_commodity_batch_search(self, batch):
        batch_objs = self.current_env['commodity.batch'].search([('batch', 'like', batch)])
        if not batch_objs:
            return rest.render_json({"status": "no", "message": "", "data": ''})
        batch_lists = []
        for batch_obj in batch_objs:
            batch_list = {}
            batch_list['id'] = batch_obj.id
            batch_list['code'] = batch_obj.code
            batch_list['name'] = batch_obj.batch
            batch_lists.append(batch_list)
        return rest.render_json({"status": "yes", "message": "", "data": batch_lists})
    #商品批次信息
    @authorizer.authorize
    @http.route('/api/kcgl/get_batch_list/<code>', type='http', auth='none', methods=['GET'])
    def get_batch_list(self, code):
        jm_code = jiemi.def_jiemi(code)
        if jm_code[15:18] == '000':
            warehouse_obj = self.current_env['warehouse.one']
        elif jm_code[15:18] != '000' and jm_code[-2:] == '00':
            warehouse_obj = self.current_env['warehouse.two']
        else:
            warehouse_obj = self.current_env['warehouse.line']
        commodity_obj = warehouse_obj.search([('type', '=', 'out'), ('start_code', '<=', jm_code), ('end_code', '>=', jm_code)])
        if not commodity_obj:
            return rest.render_json({"status": "no", "message": code, "data": ''})
        commodity_list = {}
        commodity_list['code'] = commodity_obj.line_id.batch_id.code
        commodity_list['name'] = commodity_obj.line_id.batch_id.name
        commodity_list['batch'] = commodity_obj.line_id.batch_id.batch
        commodity_list['scxh'] = commodity_obj.line_id.batch_id.messages
        commodity_list['scdate'] = commodity_obj.line_id.batch_id.production_date
        commodity_list['scjd'] = commodity_obj.line_id.batch_id.branch_id.name
        commodity_list['commodity'] = commodity_obj.line_id.commodity_id.name
        return rest.render_json({"status": "yes", "message": code, "data": commodity_list})
    #原材料批次信息123123
    @authorizer.authorize
    @http.route('/api/kcgl/get_material_batch/<code>', type='http', auth='none', methods=['GET'])
    def get_material_batch(self, code):
        jm_code = jiemi.def_jiemi(code)
        if jm_code == '0000':
            return rest.render_json({"status": "no", "message": code, "data": ''})
        if jm_code[15:18] == '000':
            warehouse_obj = self.current_env['warehouse.one']
        elif jm_code[15:18] != '000' and jm_code[-2:] == '00':
            warehouse_obj = self.current_env['warehouse.two']
        else:
            warehouse_obj = self.current_env['warehouse.line']
        commodity_obj = warehouse_obj.search([('type', '=', 'out'), ('start_code', '<=', jm_code), ('end_code', '>=', jm_code)])
        if not commodity_obj:
            return rest.render_json({"status": "no", "message": code, "data": ''})
        batch_objs = commodity_obj.line_id.batch_id.line_id
        batch_lists = []
        for batch_obj in batch_objs:
            batch_list = {}
            batch_list['code'] = batch_obj.material_batch_id.id
            batch_list['name'] = batch_obj.material_batch_id.name
            batch_list['batch'] = batch_obj.material_batch_id.batch
            batch_list['materia'] = batch_obj.material_batch_id.materia_id.name
            batch_list['supplier'] = batch_obj.material_batch_id.supplier_id.name
            batch_list['picture'] = batch_obj.material_batch_id.picture_id.image
            batch_lists.append(batch_list)
        return rest.render_json({"status": "yes", "message": code, "data": batch_lists})

    #加工过程
    @authorizer.authorize
    @http.route('/api/kcgl/get_commodity_making/<code>', type='http', auth='none', methods=['GET'])
    def get_commodity_making(self, code):
        jm_code = jiemi.def_jiemi(code)
        if jm_code == '0000':
            return rest.render_json({"status": "no", "message": code, "data": ''})
        if jm_code[15:18] == '000':
            warehouse_obj = self.current_env['warehouse.one']
        elif jm_code[15:18] != '000' and jm_code[-2:] == '00':
            warehouse_obj = self.current_env['warehouse.two']
        else:
            warehouse_obj = self.current_env['warehouse.line']
        commodity_obj = warehouse_obj.search([('type', '=', 'out'), ('start_code', '<=', jm_code), ('end_code', '>=', jm_code)])
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
            making_list['code'] = making_list_obj.id
            making_list['name'] = making_list_obj.name
            making_list['type'] = making_list_obj.type.name
            making_list['messages'] = making_list_obj.messages
            making_list['picture'] = making_list_obj.picture_id.image
            making_lists.append(making_list)
        return rest.render_json({"status": "yes", "message": code, "data": making_lists})

    #生产过程
    @authorizer.authorize
    @http.route('/api/kcgl/get_commodity_produce/<code>', type='http', auth='none', methods=['GET'])
    def get_commodity_produce(self, code):
        jm_code = jiemi.def_jiemi(code)
        if jm_code == '0000':
            return rest.render_json({"status": "no", "message": code, "data": ''})
        if jm_code[15:18] == '000':
            warehouse_obj = self.current_env['warehouse.one']
        elif jm_code[15:18] != '000' and jm_code[-2:] == '00':
            warehouse_obj = self.current_env['warehouse.two']
        else:
            warehouse_obj = self.current_env['warehouse.line']
        commodity_obj = warehouse_obj.search([('type', '=', 'out'), ('start_code', '<=', jm_code), ('end_code', '>=', jm_code)])
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
            produce_list['code'] = produce_list_obj.id
            produce_list['name'] = produce_list_obj.name
            produce_list['type'] = produce_list_obj.type.name
            produce_list['messages'] = produce_list_obj.messages
            produce_list['picture'] = produce_list_obj.picture_id.image
            produce_lists.append(produce_list)
        return rest.render_json({"status": "yes", "message": code, "data": produce_lists})

    #质检公司
    @authorizer.authorize
    @http.route('/api/kcgl/get_commodity_check/<code>', type='http', auth='none', methods=['GET'])
    def get_commodity_check(self, code):
        jm_code = jiemi.def_jiemi(code)
        if jm_code == '0000':
            return rest.render_json({"status": "no", "message": code, "data": ''})
        if jm_code[15:18] == '000':
            warehouse_obj = self.current_env['warehouse.one']
        elif jm_code[15:18] != '000' and jm_code[-2:] == '00':
            warehouse_obj = self.current_env['warehouse.two']
        else:
            warehouse_obj = self.current_env['warehouse.line']
        commodity_obj = warehouse_obj.search([('type', '=', 'out'), ('start_code', '<=', jm_code), ('end_code', '>=', jm_code)])
        if not commodity_obj:
            return rest.render_json({"status": "no", "message": code, "data": ''})
        commodity_id = commodity_obj.line_id.commodity_id.id
        check_obj = self.current_env['commodity.check.line'].search([('name', '=', commodity_id)])
        check_list_objs = check_obj.commodity_id.line_id
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
            picture_lists = []
            picture_objs = check_list_obj.picture_id
            for picture_obj in picture_objs:
                picture_list = {}
                picture_list['picture'] = picture_obj.name.image
                picture_lists.append(picture_list)
            check_list['picture'] = picture_lists
            check_lists.append(check_list)
        return rest.render_json({"status": "yes", "message": code, "data": check_lists})
# def jiemi.def_jiemi(code):
#     code = str(code)
#     str_one = code[:2]
#     str_len = 2 - len(code)
#     str_code = code[str_len:]
#     int_one = int(str_one) // 10
#     int_two = int(str_one) % 10
#     int_end = len(code) - int_two
#     b1 = ''
#     str_code = str_code[0-int_two:] + str_code[:int_end]
#     if int_one % 2 == 0:
#         for i in range(1, len(code)-2, 2):
#             b1 = b1 + str_code[i]
#     else:
#         for i in range(0, len(code)-2, 2):
#             b1 = b1 + str_code[i]
#     return b1