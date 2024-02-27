from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def create(self, vals):
        product = super(ProductTemplate, self).create(vals)
        # If product template only has one variant with no default code, assign default code
        if product.product_variant_count == 1 and product.product_variant_id.default_code is None and product.default_code:
            product.product_variant_id.default_code = product.default_code
        return product
