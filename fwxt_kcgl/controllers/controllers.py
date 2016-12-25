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
    #扫码入库
    @authorizer.authorize
    @http.route('/api/kcgl/get_kcrk/<unit_id>', type='http', auth='none', methods=['GET'])
    def get_kcrk(self, unit_id, goods_id, batch_id, code_lists):
        code = 'RKD' + date_ref[:4] + date_ref[5:7] + str(random.randint(100, 999))
        rkd_obj = self.current_env['warehouse.doc']
        company_objs = self.current_env['company.info'].search([])
        kh = ''
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
        rkd_obj_id = rkd_obj.create(values)
        list_obj = self.current_env['batch.list']
        warehouse_obj = self.current_env['warehouse.line']
        batch_lists = eval(code_lists)
        j = 0
        for batch_list in batch_lists:
            try:
                tm_code = def_decrypt(batch_list['name'])
            except:
                messages = '非法条码，不能进行扫码入库，请联系管理员！'
                return rest.render_json({'status': 'no', "message": tm_code, "data": messages})
            num = int(batch_list['number'])
            code = int(tm_code)-1
            values = {
                'code': str(batch_list['name']),
                'name': str(batch_list['name']),
                'line_id': str(rkd_obj_id.id),
                'number': int(batch_list['number']),
            }
            warehouse_line_obj = list_obj.search([('name', '=', str(batch_list['name']))])
            if not warehouse_line_obj:
                warehouse_obj.create(values)
                j = j + num
            for n in range(1, num):
                ym_code = def_encryption(code, n, kh)
                values = {
                    'code': str(code+n),
                    'name': str(ym_code),
                    'line_id': str(rkd_obj_id.id),
                    'number': 0,
                }
                batch_obj = list_obj.search([('name', '=', str(ym_code))])
                if not batch_obj:
                    list_obj.create(values)
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
        warehouse_obj = self.current_env['warehouse.line']
        list_obj = self.current_env['batch.list']
        batch_lists = eval(code_lists)
        j = 0
        for batch_list in batch_lists:
            try:
                tm_code = def_decrypt(batch_list['name'])
            except:
                messages = '非法条码，不能进行扫码出库，请联系管理员！'
                return rest.render_json({'status': 'no', "message": tm_code, "data": messages})
            num = int(batch_list['number'])
            code = int(tm_code)-1
            values = {
                'code': str(batch_list['name']),
                'name': str(batch_list['name']),
                'line_id': str(rkd_obj_id.id),
                'number': int(batch_list['number']),
            }
            warehouse_line_obj = list_obj.search([('name', '=', str(batch_list['name']))])
            if not warehouse_line_obj:
                warehouse_obj.create(values)
                j = j + num
            for n in range(1, num):
                values = {
                    'code': str(code+n),
                    'name': str(code+n),
                    'out_id': str(rkd_obj_id.id),
                }
                batch_obj = list_obj.search([('name', '=', str(code+n))])
                if batch_obj:
                    batch_obj.update({'out_id': str(rkd_obj_id.id)})
                else:
                    list_obj.create(values)
        rkd_obj_id.update({'number': j})
        return rest.render_json({"status": "yes", "message": code, "data": code_lists})
    #查询
    @authorizer.authorize
    @http.route('/api/kcgl/get_search/<tm_code>', type='http', auth='none', methods=['GET'])
    def get_search(self, tm_code):
        if not tm_code:
            messages = '二维码损坏，无法正确获取到条码信息！'
            return rest.render_json({"status": "yes", "message": tm_code, "data": messages})
        else:
            try:
                code = def_decrypt(tm_code)
            except:
                messages = '该产品不是本公司产品请联系公司'
                return rest.render_json({'status': 'no', "message": tm_code, "data": messages})
            company_objs = self.current_env['company.info'].search([])
            if company_objs:
                for company_obj in company_objs:
                    company_code = company_obj.company_code
                len_code = len(company_code)
                if company_code != code[:len_code]:
                    messages = '该产品不是本公司产品请联系公司'
                    return rest.render_json({'status': 'no', "message": tm_code, "data": messages})
            else:
                messages = '请在公司简介中维护公司信息及公司编码！'
                return rest.render_json({"status": "yes", "message": tm_code, "data": messages})
        batch_list_obj = self.current_env['batch.list'].search([('code', '=', code)])
        # print batch_list_obj,batch_list_obj.id,code,tm_code
        messages = ''
        if not batch_list_obj:
            messages = '该产品不是本公司产品请联系公司'
        if batch_list_obj.number == 0:
            batch_list_obj.update({'number': batch_list_obj.number + 1})
            messages = '这是第一次查询,您所查询的是公司的产品,是正品,谢谢使用。'
        else:
            messages = '您所查询的是公司的产品,但经过多次查询，请及时联系客服验证真假！'
            number = int(batch_list_obj.messages)+1
            batch_list_obj.update({'messages': str(number)})
        return rest.render_json({"status": "yes", "message": tm_code, "data": messages})
def def_decrypt(code):
    code = str(code)
    str_one = code[:2]
    str_len = 2 - len(code)
    str_code = code[str_len:]
    int_one = int(str_one) // 10
    int_two = int(str_one) % 10
    int_end = len(code) - int_two
    b1 = ''
    str_code = str_code[0-int_two:] + str_code[:int_end]
    if int_one % 2 == 0:
        for i in range(1, len(code)-2, 2):
            b1 = b1 + str_code[i]
    else:
        for i in range(0, len(code)-2, 2):
            b1 = b1 + str_code[i]
    return b1
def def_encryption(code, num, kh):
    gd = len(str(code))
    str_bs = '000000000000000000'
    str_num = '100000000000000000000'
    ws = gd
    min_str = str_num[:ws]
    max_str = str_num[:ws+1]
    min_num = int(min_str) + num
    max_num = int(max_str) - 1
    #随机取两位数
    one = random.randint(10, 99)
    #求10的商和余数
    int_one = one // 10
    int_two = one % 10
    #随机取8位数
    sj = random.randint(min_num, max_num)
    #转换程字符床
    str1 = str(sj)
    #加上客户数字 凑齐8位 不够的中间补0
    str_code = (str_bs+str(num))
    cd = 0-(ws - len(str(kh)))
    str2 = str(kh)+str_code[cd:]
    str3 = ''
    #根据随机的二位树 第一位是奇数还是偶数
    for j in range(0, gd):
        if int_one % 2 == 0:
            str3 = str3 + str1[j] + str2[j]
        else:
            str3 = str3 + str2[j] + str1[j]
    #根据随机的二位数，惊醒左右转换
    int_end = int_two - gd*2
    str3 = str3[int_end:] + str3[:int_two]
    str4 = str(one) + str3
    return str4