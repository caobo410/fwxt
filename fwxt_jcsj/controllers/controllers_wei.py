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
    # 获取单位
    @authorizer.authorize
    @http.route('/api/jcsj/get_picture/<type>', type='http', auth='none', methods=['POST'])
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
            print picture_lists
        return rest.render_json({"status": "yes", "message": type, "data": picture_lists})