from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ProductProduct(models.Model):
    _inherit = "product.product"

    default_orderpoint_id = fields.Many2one(comodel_name='stock.warehouse.orderpoint', string="Automatically created reordering rule")
    
    def _update_default_orderpoint(self):
        if self.default_orderpoint_id:
            self.default_orderpoint_id._update_external_id()
        else:
            self.default_orderpoint_id = self.env['stock.warehouse.orderpoint'].create({
                'product_id': self.id, 
                'trigger': 'manual'
            })
            try:
                self.default_orderpoint_id._update_external_id()
            except Exception as v:
                raise UserError(_("Only one reordering rule can be created per product."))

    @api.model
    def create(self, vals):
        product = super(ProductProduct, self).create(vals)
        if product.default_code:
            product._update_default_orderpoint()
        return product

    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        if vals.get('default_code'):
            self._update_default_orderpoint()
        return res
