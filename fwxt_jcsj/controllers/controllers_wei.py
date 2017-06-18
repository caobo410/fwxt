# -*- coding: utf-8 -*-
from openerp import http
from openerp import http, fields
import authorizer
import rest
import jiemi
from datetime import datetime

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


date_ref = datetime.now().strftime('%Y-%m-%d')
# _logger = logging.getLogger(__name__)

class OrderController(http.Controller):
    # 获取图片
    @authorizer.authorize
    @http.route('/api/jcsj/get_picture/<type>', type='http', auth='none', methods=['GET'])
    def get_picture(self, type):
        if type == 'head':
            picture_objs = self.current_env['picture.management'].search([('type', '=', 'head')])
        elif type == 'boby':
            picture_objs = self.current_env['picture.management'].search([('type', '=', 'boby')])
        elif type == 'other':
            picture_objs = self.current_env['picture.management'].search([('type', '=', 'other')])
        else:
            picture_objs = self.current_env['picture.management'].search([('type', '=', 'head')])
        if not picture_objs:
            return rest.render_json({"status": "no", "message": type, "data": ''})
        picture_lists = []
        for picture_obj in picture_objs:
            picture_list = {}
            picture_list['id'] = picture_obj.id
            picture_list['code'] = picture_obj.code
            picture_list['name'] = picture_obj.name
            picture_list['image'] = picture_obj.image
            picture_lists.append(picture_list)
        return rest.render_json({"status": "yes", "message": type, "data": picture_lists})
    # 联系我们
    @authorizer.authorize
    @http.route('/api/jcsj/get_company/<company>', type='http', auth='none', methods=['GET'])
    def get_company(self, company):
        company_objs = self.current_env['company.info'].search([])
        if not company_objs:
            return rest.render_json({"status": "no", "message": company, "data": ''})
        company_lists = []
        for company_obj in company_objs:
            company_list = {}
            company_list['name'] = company_obj.name
            company_list['people'] = company_obj.contacts_people
            company_list['phone'] = company_obj.tel
            company_list['wetch'] = company_obj.wetch
            company_list['address'] = company_obj.address
            company_list['qq'] = company_obj.qq
            company_list['web'] = company_obj.website
            company_lists.append(company_list)
        return rest.render_json({"status": "yes", "message": company, "data": company_lists})

    #商品信息
    @authorizer.authorize
    @http.route('/api/jcsj/get_commodity_list/<commodity>', type='http', auth='none', methods=['GET'])
    def get_commodity_list(self, commodity):
        commodity_objs = self.current_env['commodity.info'].search([])
        if not commodity_objs:
            return rest.render_json({"status": "no", "message": commodity, "data": ''})
        commodity_lists = []
        for commodity_obj in commodity_objs:
            commodity_list = {}
            commodity_list['name'] = commodity_obj.name
            commodity_list['image'] = commodity_obj.image
            line_lists = []
            if len(commodity_obj.line_id) > 0:
                for line in commodity_obj.line_id:
                    line_list = {}
                    line_list['name'] = line.name + ':' + line.messages
                    line_lists.append(line_list)
                commodity_list['list'] = line_lists
            else:
                commodity_list['list'] = {}
            commodity_lists.append(commodity_list)
        return rest.render_json({"status": "yes", "message": commodity, "data": commodity_lists})

    #查看出入库信息
    @authorizer.authorize
    @http.route('/api/jcsj/get_agent_list/<password>', type='http', auth='none', methods=['GET'])
    def get_agent_list(self, password, code):
        password_objs = self.current_env['other.info'].search([('password', '=', password)])
        jm_code = jiemi.def_jiemi(code)
        if jm_code == '0000':
            return rest.render_json({"status": "no", "message": code, "data": ''})
        rk_obj = self.current_env['warehouse.line'].search([('type', '=', 'in'), ('start_code', '<=', jm_code), ('end_code', '>=', jm_code)])
        ck_obj = self.current_env['warehouse.line'].search([('type', '=', 'out'), ('start_code', '<=', jm_code), ('end_code', '>=', jm_code)])
        if not password_objs:
            return rest.render_json({"status": "no", "message": password, "data": 'Password Error!'})
        batch_objs = self.current_env['batch.list'].search([('name', '=', code)])
        agent_list = {}
        agent_list['rk_code'] = rk_obj.line_id.code
        agent_list['rk_date'] = rk_obj.line_id.date_confirm
        agent_list['ck_code'] = ck_obj.line_id.code
        agent_list['ck_date'] = ck_obj.line_id.date_confirm
        agent_list['area'] = ck_obj.line_id.agent_id.area
        agent_list['agent'] = ck_obj.line_id.agent_id.name
        agent_list['express'] = ck_obj.line_id.express_id.name
        agent_list['express_code'] = ck_obj.line_id.express_code
        return rest.render_json({"status": "yes", "message": password, "data": agent_list})
    #企业介绍
    @authorizer.authorize
    @http.route('/api/jcsj/get_company_list/<code>', type='http', auth='none', methods=['GET'])
    def get_company_list(self, code):
        company_objs = self.current_env['company.info'].search([])
        if not company_objs:
            return rest.render_json({"status": "no", "message": code, "data": 'Password Error!'})
        for company_obj in company_objs:
            company_list = company_obj.company_info
        return rest.render_json({"status": "yes", "message": code, "data": company_list})
    #获取公众号
    @authorizer.authorize
    @http.route('/api/jcsj/get_wechat/<wechat>', type='http', auth='none', methods=['GET'])
    def get_wechat(self, wechat):
        wechat_objs = self.current_env['other.info'].search([])
        if not wechat_objs:
            return rest.render_json({"status": "no", "message": wechat, "data": u'请维护其他信息中心的微信公众号!'})
        for wechat_obj in wechat_objs:
            wechar_account = wechat_obj.wechat_account
        return rest.render_json({"status": "yes", "message": wechat, "data": wechar_account})
    #视频
    @authorizer.authorize
    @http.route('/api/jcsj/get_mp4/<type>', type='http', auth='none', methods=['GET'])
    def get_mp4(self, type, code):
        if type == 'ycl':
            file_obj = self.current_env['material.batch'].search([('id', '=', int(code))])
            if not file_obj:
                return rest.render_json({"status": "no", "message": code, "data": u'code参数有问题，请联系管理员'})
            video_obj = file_obj.file_id
        elif type == 'sc':
            file_obj = self.current_env['produce.line'].search([('id', '=', int(code))])
            if not file_obj:
                return rest.render_json({"status": "no", "message": code, "data": u'code参数有问题，请联系管理员'})
            video_obj = file_obj.video_id
        elif type == 'jg':
            file_obj = self.current_env['making.line'].search([('id', '=', int(code))])
            if not file_obj:
                return rest.render_json({"status": "no", "message": code, "data": u'code参数有问题，请联系管理员'})
            video_obj = file_obj.video_id
        if not video_obj:
            return rest.render_json({"status": "no", "message": code, "data": u'code的单据没有维护视频信息，请联系管理员'})
        path = video_obj.store_fname
        # filepath = '/home/xinyi/.local/share/Odoo/filestore/fwxt/' +path
        filepath = '/usr/lhd/.local/share/Odoo/filestore/fwxt/' +path
        filename = video_obj.datas_fname
        return rest.sendfile(filepath, filename)

# def def_decrypt(code):
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

