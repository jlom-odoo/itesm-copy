from odoo import fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    parent_location_id = fields.Many2one('stock.location', related='location_id.location_id', store=True)

    def _apply_inventory(self):
        group_by = self.read_group([('location_id.is_count_location', '=', True), ('parent_location_id.usage', '!=', 'view')],
                                   ['inventory_quantity', 'lot_id', 'package_id'], ['parent_location_id', 'product_id', 'lot_id', 'package_id'], lazy=False)
        vals_list = []
        for quant in group_by:
            vals_list.append({
                'product_id': quant['product_id'][0],
                'location_id': quant['parent_location_id'][0],
                'inventory_quantity': quant['inventory_quantity'],
                'lot_id': quant['lot_id'] and quant['lot_id'][0] or False,
                'package_id': quant['package_id'] and quant['package_id'][0] or False
            })
        if vals_list:
            new_quants = super().create(vals_list)
            ungrouped_quants = self.filtered(lambda q: q.location_id.is_count_location == False or q.parent_location_id.usage == 'view')  # nopep8
            super(StockQuant, ungrouped_quants + new_quants)._apply_inventory()
            (self - ungrouped_quants).action_set_inventory_quantity_to_zero()
            (self - ungrouped_quants).write({'user_id': False})
            new_quants.action_set_inventory_quantity_to_zero()
            (self + new_quants)._merge_quants()
        else:
            super(StockQuant, self)._apply_inventory()
