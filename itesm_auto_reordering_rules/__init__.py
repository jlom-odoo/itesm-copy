from odoo import api, SUPERUSER_ID
from . import models

def update_orderpoint_external_ids(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Remove all existing orderpoints
    orderpoints = env['stock.warehouse.orderpoint'].search([])
    orderpoints.unlink()
    # Remove all external ids for orderpoints
    orderpoints_external_ids = env['ir.model.data'].search([
        ('model', '=', 'stock.warehouse.orderpoint')
    ])
    orderpoints_external_ids.unlink()
    # Create new orderpoints for existing products
    products = env['product.product'].search([])
    for product in products:
        if product.company_id and product.default_code:
            warehouse_id = env['stock.warehouse'].search([
                ('company_id', '=', product.company_id.id)
            ], limit=1)
            product.default_orderpoint_id = env['stock.warehouse.orderpoint'].sudo().create({
                'product_id': product.id, 
                'company_id': product.company_id.id,
                'warehouse_id': warehouse_id.id
            })
        elif product.default_code:
            product.default_orderpoint_id = env['stock.warehouse.orderpoint'].sudo().create({
                'product_id': product.id, 
            })
