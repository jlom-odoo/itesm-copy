from odoo import api, SUPERUSER_ID
from . import models

def update_orderpoint_external_ids(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    external_ids = env['ir.model.data'].search([
        ('model', '=', 'stock.warehouse.orderpoint')
    ])
    for external_id in external_ids:
        reordering_rule = env['stock.warehouse.orderpoint'].browse([external_id.res_id]).exists()
        if reordering_rule.product_id.default_code and external_id.name != f"id_rr_{reordering_rule.product_id.default_code}":
            external_id.name = f"id_rr_{reordering_rule.product_id.default_code}"
