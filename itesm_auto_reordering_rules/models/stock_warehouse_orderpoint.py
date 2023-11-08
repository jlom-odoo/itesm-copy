from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"
    default_external_id = fields.Many2one(comodel_name='ir.model.data', string='Default external id')


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
        if not orderpoint.product_id.default_code:
            raise UserError(_("A reordering rule cannot be created for a product without a default code."))
        try:
            orderpoint._update_external_id()
        except Exception as v:
            raise UserError(_("Only one reordering rule can be created per product."))
        return orderpoint
