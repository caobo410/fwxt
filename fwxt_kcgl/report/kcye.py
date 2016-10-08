# -*- coding: utf-8 -*-

from openerp import tools
import openerp.addons.decimal_precision as dp
from openerp import models, fields

class report_stock_kcye(models.Model):
    _name = "report.stock.kcye"
    _auto = False

    commodity = fields.Char(string='Commodity', help="Commodity")
    commodity_id = fields.Many2one('commodity.info', string='Commodity', help="Messages")
    unit = fields.Char(string='Unit', help='Unit')
    batch = fields.Char(string='Batch', help='Batch')
    warehouse = fields.Char(string='Warehouse', help='Warehouse')
    commodity_num = fields.Float(string='数量', digits_compute=dp.get_precision('Quantity'))

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_stock_kcye')
        cr.execute(
            """
            create or replace view report_stock_kcye as (
                   select commodity_info.name as commodity,warehouse_info.name as warehouse,rk.commodity_id as commodity_id,
                          commodity_batch.name as batch, base_unit.name as unit, sum(rknum-cknum) as commodity_num
                    from (
                        select warehouse_id,commodity_id,batch_id,unit_id,sum(number) as rknum
                        from warehouse_doc
                        where type ='in' and number>0
                        group by warehouse_id,commodity_id,batch_id) as rk
                    left join
                        (select warehouse_id,commodity_id,batch_id,unit_id,sum(number) as cknum
                         from warehouse_doc
                         where type ='out' and number>0
                         group by warehouse_id,commodity_id,batch_id) as ck
                         on rk.warehouse_id=ck.warehouse_id
                         and rk.commodity_id= ck.commodity_id
                         and rk.batch_id=ck.batch_id
                    left join commodity_info on commodity_info.id = rk.commodity_id
                    left join warehouse_info on warehouse_info.id = rk.warehouse_id
                    left join commodity_batch on commodity_batch.id = rk.batch_id
                    left join base_unit on base_unit.id = rk.unit_id
                group by commodity_info.name,warehouse_info.name,rk.commodity_id,rk.batch_id
                order by commodity_info.name,warehouse_info.name asc
                            )
        """)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
