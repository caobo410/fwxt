# -*- coding: utf-8 -*-
from openerp import http
from openerp import http, fields
import authorizer
import rest
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
        company_objs = self.current_env['res.company'].search([])
        if not company_objs:
            return rest.render_json({"status": "no", "message": company, "data": ''})
        company_lists = []
        for company_obj in company_objs:
            company_list = {}
            company_list['name'] = company_obj.name
            company_list['phone'] = company_obj.phone
            company_list['fax'] = company_obj.fax
            company_list['email'] = company_obj.email
            company_list['province'] = company_obj.state_id.name
            company_list['city'] = company_obj.city
            company_list['street'] = company_obj.street
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

    #生产基地
    @authorizer.authorize
    @http.route('/api/jcsj/get_agent_list/<password>', type='http', auth='none', methods=['GET'])
    def get_agent_list(self, password, code):
        password_objs = self.current_env['other.info'].search([('password', '=', password)])
        if not password_objs:
            return rest.render_json({"status": "no", "message": password, "data": 'Password Error!'})
        batch_objs = self.current_env['batch.list'].search([('code', '=', code)])
        agent_name = batch_objs.line_id.agent_id.name
        return rest.render_json({"status": "Yes", "message": password, "data": agent_name})
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
    #企业介绍
    @authorizer.authorize
    @http.route('/api/jcsj/get_mp4/<type>', type='http', auth='none', methods=['GET'])
    def get_company_list(self, type, code):
        if type =='ycl':
            file_obj = self.current_env['material.batch'].search([('id', '=', int(code))])
            video_obj = file_obj.file_id
        elif type =='sc':
            file_obj = self.current_env['produce.line'].search([('id', '=', int(code))])
            video_obj = file_obj.video_obj
        elif type =='jg':
            file_obj = self.current_env['making.line'].search([('id', '=', int(code))])
            video_obj = file_obj.video_obj
        path = video_obj.store_fname
        path = path.replace('/', '\\')
        filepath = 'D:\\odoo-8.0\\project\\fwxt\datafile\\filestore\\fwxt\\' +path
        print filepath
        # filepath = '/usr/lhd/.local/share/Odoo/filestore/fwxt/' +path
        filename = video_obj.datas_fname
        print filename
        return rest.sendfile(filepath, filename)

