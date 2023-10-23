from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = "product.product"

    reordering_rule_ir_model_data_id = fields.Many2one(comodel_name='ir.model.data')

    def _create_orderpoint(self):
        self.ensure_one()
        return self.env['stock.warehouse.orderpoint'].create({
            'product_id': self.id, 
            'product_min_qty': 0, 
            'product_max_qty': 0
        })
    
    def _link_orderpoint_to_external_id(self, orderpoint_id):
        self.ensure_one()
        self.reordering_rule_ir_model_data_id = self.env['ir.model.data'].create({
            'module': '_export_', 
            'name': f"id_rr_{self.default_code}", 
            'model': 'stock.warehouse.orderpoint', 
            'res_id': orderpoint_id
        })

    @api.model
    def create(self, vals):
        product = super(ProductProduct, self).create(vals)
        if product.default_code:
            new_ordering_rule_id = product._create_orderpoint()
            product._link_orderpoint_to_external_id(new_ordering_rule_id)
        return product

    @api.onchange('default_code')
    def _default_code_change(self):
        self.ensure_one()
        if self.orderpoint_ids and self.reordering_rule_ir_model_data_id:
            self.reordering_rule_ir_model_data_id.write({
                'name': f"id_rr_{self.default_code}",
            })
