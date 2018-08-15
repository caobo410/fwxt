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
import jiemi
import random
import datetime
date_ref = datetime.datetime.now().strftime('%Y-%m-%d')
def get_kcrk(self, unit_id, goods_id, batch_id, code_lists):
    #print code_lists
    rk_code = ''
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
            return messages
        #判断code的9-12位置是否000，如果为000 ，需要存储托盘
        # print type(batch_code)
        if batch_code[15:18] == '000':
            warehouse_one_obj = self.current_env['warehouse.one']
            batch_obj = warehouse_one_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', 'in')])
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
            values={
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
            #插入箱号
            for i in range(1, int(num_one) + 1):
                bs_code = '000'+str(i)
                bs_code = bs_code[-3:]
                end_str ='000'+str(int(num_two))
                xh_code = batch_code[:15] + bs_code + batch_code[18:-2] + '00'
                start_code = batch_code[:15] + bs_code + batch_code[18:-2] + '01'
                end_code = batch_code[:15] + bs_code + batch_code[18:-2] + end_str[-2:]
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
                batch_obj = batch_list_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', 'in')])
                if not batch_obj:
                    batch_list_obj.create(values)
                    rkd_obj_id.update({'number': int(rkd_obj_id.number) + 1})
        elif batch_code[15:18] != '000' and batch_code[-2:] == '00':
            warehouse_obj = self.current_env['warehouse.two']
            batch_obj = warehouse_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', 'in')])
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
            for i in range(1, int(num) + 1):
                j = i + int(batch_code[15:18]) - 1
                bs_code = '000'+str(j)
                bs_code = bs_code[-3:]
                end_str ='000'+str(int(num_one))
                xh_code = batch_code[:15] + bs_code + batch_code[18:-2] + '00'
                start_code = batch_code[:15] + bs_code + batch_code[18:-2] + '01'
                end_code = batch_code[:15] + bs_code + batch_code[18:-2] + end_str[-2:]
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
                batch_obj = batch_list_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', 'in')])
                if not batch_obj:
                    batch_list_obj.create(values)
                    rkd_obj_id.update({'number': int(rkd_obj_id.number) + 1})
        else:
            warehouse_obj = self.current_env['warehouse.line']
            batch_obj = warehouse_obj.search([('start_code', '<=', batch_code), ('end_code', '>=', batch_code), ('type', '=', 'in')])
            if not batch_obj:
                j = int(batch_code[-2:]) + int(num) - 1
                bs_code = '00'+str(j)
                values = {
                        'code': str(batch_code),
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
        messages = u'出库完成!'
    return messages

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: