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
    #http://localhost:8069/api/jcsj/get_batch/batch
    @authorizer.authorize
    @http.route('/api/batch/get_commodity_batch/<batch>', type='http', auth='none', methods=['POST'])
    def get_commodity_batch(self, batch):
        batch_objs = self.current_env['commodity.batch'].search([])
        if not batch_objs:
            return rest.render_json({"status": "no", "message": "", "data": ''})
        batch_lists = []
        for batch_obj in batch_objs:
            batch_list = {}
            batch_list['id'] = batch_obj.id
            batch_list['code'] = batch_obj.code
            batch_list['name'] = batch_obj.name
            batch_lists.append(batch_list)
        return rest.render_json({"status": "yes", "message": "", "data": batch_lists})