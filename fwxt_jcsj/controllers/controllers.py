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
    # 登录验证
    #/api/jcsj/login_in/ERP?login=admin&password=1
    #@authorizer.authorize
    @http.route('/api/jcsj/login_in/<database>', type='http', auth='none', methods=['GET'])
    def login_in(self, database, login, password):
        print '234'
        uid = http.request.session.authenticate(database, login, password)
        print uid
        if not uid:
            return rest.render_json({"status": "yes", "message": "", "data": 'Password error'})
        return rest.render_json({"status": "yes", "message": "", "data": 'Welcome'})
    # 获取单位
    #http://localhost:8069/api/jcsj/get_unit/unit
    @authorizer.authorize
    @http.route('/api/jcsj/get_unit/<code>', type='http', auth='none', methods=['GET'])
    def get_unit(self, code):
        unit_objs = self.current_env['base.unit'].search([])
        if not unit_objs:
            return rest.render_json({"status": "no", "message": "", "data": ''})
        unit_lists=[]
        for unit_obj in unit_objs:
            unit_list = {}
            unit_list['id'] = unit_obj.id
            unit_list['code'] = unit_obj.code
            unit_list['name'] = unit_obj.name
            unit_lists.append(unit_list)
        return rest.render_json({"status": "yes", "message": "", "data": unit_lists})
    # 获取商品
    #http://localhost:8069/api/jcsj/get_unit/unit
    @authorizer.authorize
    @http.route('/api/jcsj/get_commodity/<commodity>', type='http', auth='none', methods=['GET'])
    def get_commodity(self, commodity):
        commodity_objs = self.current_env['commodity.info'].search([])
        if not commodity_objs:
            return rest.render_json({"status": "no", "message": "", "data": ''})
        commodity_lists=[]
        for commodity_obj in commodity_objs:
            commodity_list={}
            commodity_list['id'] = commodity_obj.id
            commodity_list['code'] = commodity_obj.code
            commodity_list['name'] = commodity_obj.name
            commodity_lists.append(commodity_list)
        return rest.render_json({"status": "yes", "message": "", "data": commodity_lists})
    # 获取快递
    #http://localhost:8069/api/jcsj/get_unit/unit
    @authorizer.authorize
    @http.route('/api/jcsj/get_express_info/<express>', type='http', auth='none', methods=['GET'])
    def get_express_info(self, express):
        express_objs = self.current_env['express.info'].search([])
        if not express_objs:
            return rest.render_json({"status": "no", "message": "", "data": ''})
        express_lists = []
        for express_obj in express_objs:
            express_list = {}
            express_list['id'] = express_obj.id
            express_list['code'] = express_obj.code
            express_list['name'] = express_obj.name
            express_lists.append(express_list)
        return rest.render_json({"status": "yes", "message": "", "data": express_lists})
    # 获取经销商
    #http://localhost:8069/api/jcsj/get_agent_info/unit
    @authorizer.authorize
    @http.route('/api/jcsj/get_agent_info/<commodity>', type='http', auth='none', methods=['GET'])
    def get_agent_info(self, commodity):
        agent_objs = self.current_env['agent.info'].search([])
        if not agent_objs:
            return rest.render_json({"status": "no", "message": "", "data": ''})
        agent_lists = []
        for agent_obj in agent_objs:
            agent_list = {}
            agent_list['id'] = agent_obj.id
            agent_list['code'] = agent_obj.code
            agent_list['name'] = agent_obj.name
            agent_lists.append(agent_list)
        return rest.render_json({"status": "yes", "message": "", "data": agent_lists})