from collections import defaultdict
from dateutil import relativedelta

from odoo import SUPERUSER_ID, _, api, fields, models, registry
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, frozendict, split_every

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
        
        if not orderpoint.product_id.default_code:
            raise UserError(_("A reordering rule cannot be created for a product without a default code."))
        try:
            orderpoint._update_external_id()
        except Exception as v:
            raise UserError(_("Only one reordering rule can be created per product."))
        return orderpoint

    def _get_orderpoint_action(self):
        """Create manual orderpoints for missing product in each warehouses. It also removes
        orderpoints that have been replenish. In order to do it:
        - It uses the report.stock.quantity to find missing quantity per product/warehouse
        - It checks if orderpoint already exist to refill this location.
        - It checks if it exists other sources (e.g RFQ) tha refill the warehouse.
        - It creates the orderpoints for missing quantity that were not refill by an upper option.

        return replenish report ir.actions.act_window
        """
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_orderpoint_replenish")
        action['context'] = self.env.context
        # Search also with archived ones to avoid to trigger product_location_check SQL constraints later
        # It means that when there will be a archived orderpoint on a location + product, the replenishment
        # report won't take in account this location + product and it won't create any manual orderpoint
        # In master: the active field should be remove
        orderpoints = self.env['stock.warehouse.orderpoint'].with_context(active_test=False).search([])
        # Remove previous automatically created orderpoint that has been refilled.
        orderpoints_removed = orderpoints._unlink_processed_orderpoints()
        orderpoints = orderpoints - orderpoints_removed
        to_refill = defaultdict(float)
        all_product_ids = self._get_orderpoint_products()
        all_replenish_location_ids = self.env['stock.location'].search([('replenish_location', '=', True)])
        ploc_per_day = defaultdict(set)
        # For each replenish location get products with negative virtual_available aka forecast
        for loc in all_replenish_location_ids:
            for product in all_product_ids.with_context(location=loc.id):
                if float_compare(product.virtual_available, 0, precision_rounding=product.uom_id.rounding) >= 0:
                    continue
                # group product by lead_days and location in order to read virtual_available
                # in batch
                rules = product._get_rules_from_location(loc)
                lead_days = rules.with_context(bypass_delay_description=True)._get_lead_days(product)[0]
                ploc_per_day[(lead_days, loc)].add(product.id)

        # recompute virtual_available with lead days
        today = fields.datetime.now().replace(hour=23, minute=59, second=59)
        for (days, loc), product_ids in ploc_per_day.items():
            products = self.env['product.product'].browse(product_ids)
            qties = products.with_context(
                location=loc.id,
                to_date=today + relativedelta.relativedelta(days=days)
            ).read(['virtual_available'])
            for (product, qty) in zip(products, qties):
                if float_compare(qty['virtual_available'], 0, precision_rounding=product.uom_id.rounding) < 0:
                    to_refill[(qty['id'], loc.id)] = qty['virtual_available']
            products.invalidate_recordset()
        if not to_refill:
            return action

        # Remove incoming quantity from other origin than moves (e.g RFQ)
        product_ids, location_ids = zip(*to_refill)
        qty_by_product_loc, dummy = self.env['product.product'].browse(product_ids)._get_quantity_in_progress(location_ids=location_ids)
        rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        # Group orderpoint by product-location
        orderpoint_by_product_location = self.env['stock.warehouse.orderpoint']._read_group(
            [('id', 'in', orderpoints.ids)],
            ['product_id', 'location_id', 'qty_to_order:sum'],
            ['product_id', 'location_id'], lazy=False)
        orderpoint_by_product_location = {
            (record.get('product_id')[0], record.get('location_id')[0]): record.get('qty_to_order')
            for record in orderpoint_by_product_location
        }
        for (product, location), product_qty in to_refill.items():
            qty_in_progress = qty_by_product_loc.get((product, location)) or 0.0
            qty_in_progress += orderpoint_by_product_location.get((product, location), 0.0)
            # Add qty to order for other orderpoint under this location.
            if not qty_in_progress:
                continue
            to_refill[(product, location)] = product_qty + qty_in_progress
        to_refill = {k: v for k, v in to_refill.items() if float_compare(
            v, 0.0, precision_digits=rounding) < 0.0}

        # With archived ones to avoid `product_location_check` SQL constraints
        orderpoint_by_product_location = self.env['stock.warehouse.orderpoint'].with_context(active_test=False)._read_group(
            [('id', 'in', orderpoints.ids)],
            ['product_id', 'location_id', 'ids:array_agg(id)'],
            ['product_id', 'location_id'], lazy=False)
        orderpoint_by_product_location = {
            (record.get('product_id')[0], record.get('location_id')[0]): record.get('ids')[0]
            for record in orderpoint_by_product_location
        }

        orderpoint_values_list = []
        for (product, location_id), product_qty in to_refill.items():
            orderpoint_id = orderpoint_by_product_location.get((product, location_id))
            if orderpoint_id:
                self.env['stock.warehouse.orderpoint'].browse(orderpoint_id).qty_forecast += product_qty
            else:
                orderpoint_values = self.env['stock.warehouse.orderpoint']._get_orderpoint_values(product, location_id)
                location = self.env['stock.location'].browse(location_id)
                orderpoint_values.update({
                    'name': _('Replenishment Report'),
                    'warehouse_id': location.warehouse_id.id or self.env['stock.warehouse'].search([('company_id', '=', location.company_id.id)], limit=1).id,
                    'company_id': location.company_id.id,
                })
                orderpoint_values_list.append(orderpoint_values)

        return action
