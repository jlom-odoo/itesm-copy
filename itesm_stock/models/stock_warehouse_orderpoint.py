from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"
    default_external_id = fields.Many2one(comodel_name='ir.model.data', string='Default external id')
    location_warehouse_id = fields.Integer(string="Location Warehouse ID", related="location_id.warehouse_id.id")


    def _update_external_id(self):
        if self.default_external_id:
            self.default_external_id.name = f"id_rr_{self.product_id.default_code}"
        else:
            self.default_external_id = self.env['ir.model.data'].create({
                'module': '__export__', 
                'name': f"id_rr_{self.product_id.default_code}",
                'model': 'stock.warehouse.orderpoint', 
                'res_id': self.id
            })

    @api.model
    def create(self, vals):
        orderpoint = super(StockWarehouseOrderpoint, self).create(vals)
        # Ignore if manual orderpoint
        # - Allow creating without a product's default code
        # - Allow creating multiple per product
        if orderpoint.trigger == 'manual':
            return orderpoint

        if not orderpoint.product_id.default_code:
            raise UserError(_("A reordering rule cannot be created for a product without a default code."))
        return orderpoint