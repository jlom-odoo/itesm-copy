from odoo import fields, models


class StockRoute(models.Model):
    _inherit = 'stock.route'
    
    is_backoffice_route = fields.Boolean(string="Back-office")
