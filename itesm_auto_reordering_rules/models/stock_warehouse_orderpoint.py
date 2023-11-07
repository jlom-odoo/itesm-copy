from odoo import api, fields, models
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
            raise UserError("No se puede crear una orden de reabastecimiento sin referencia interna en el producto.")
        try:
            orderpoint._update_external_id()
        except Exception as v:
            raise UserError("No se puede crear más de una orden de reabastecimiento para la misma referencia interna.")
        return orderpoint
