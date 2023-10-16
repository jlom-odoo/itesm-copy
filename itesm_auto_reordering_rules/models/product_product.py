from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = "product.product"

    default_orderpoint_id = fields.Many2one(comodel_name='stock.warehouse.orderpoint', string="Automatically created reordering rule")
    default_orderpoint_external_id = fields.Many2one(comodel_name='ir.model.data', string="Ir model data associated with the default reordering rule")

    def _update_default_orderpoint_external_id(self):
        if self.default_orderpoint_external_id:
            self.default_orderpoint_external_id.name = f"id_rr_{self.default_code}"
        else:
            self.default_orderpoint_external_id = self.env['ir.model.data'].create({
                'module': '__export__', 
                'name': f"id_rr_{self.default_code}",
                'model': 'stock.warehouse.orderpoint', 
                'res_id': self.default_orderpoint_id
            })

    @api.model
    def create(self, vals):
        product = super(ProductProduct, self).create(vals)
        product.default_orderpoint_id = self.env['stock.warehouse.orderpoint'].create({
            'product_id': product.id, 
        })
        if product.default_code:
            product._update_default_orderpoint_external_id()
        return product

    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        if vals.get('default_code'):
            self._update_default_orderpoint_external_id()
        return res
