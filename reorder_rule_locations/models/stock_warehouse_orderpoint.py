from odoo import fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'
    
    location_warehouse_id = fields.Integer(string="Location Warehouse ID", related="location_id.warehouse_id.id")
