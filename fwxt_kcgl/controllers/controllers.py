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

# class OrderController(http.Controller):
#     # 成品管理-出库
#     @authorizer.authorize
#     @http.route('/api/cpgl/cprk/<database>',  type='http', auth='none', methods=['post'])
#     def get_commodity_batch(self, batch):
#         batch_objs = self.current_env['commodity.batch'].search([])
#         if not batch_objs:
#             return rest.render_json({"status": "no", "message": ""})
#         batch_lists = []
#         for batch_obj in batch_objs:
#             batch_list = {}
#             batch_list['id'] = batch_obj.id
#             batch_list['code'] = batch_obj.code
#             batch_list['name'] = batch_obj.name
#             batch_lists.append(batch_list)
#         print batch_lists
#         return rest.render_json({"status": "yes", "message": ""})
