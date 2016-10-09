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
    # 成品管理-出库
    @authorizer.authorize
    @http.route('/api/jcsj/cprk/<database>',  type='http', auth='none', methods=['post'])
    def cpgl_cprk(self, database, login, password, packing_code):

        return rest.render_json(wlzd_mx)
