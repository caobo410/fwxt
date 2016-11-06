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

