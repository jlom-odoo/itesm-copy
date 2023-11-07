import odoo.tests
import logging

_logger = logging.getLogger(__name__)


class TestStockQuant(odoo.tests.common.TransactionCase):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass()

        cls.warehouse_id = cls.env['stock.warehouse'].create({
            'name': 'Tec Store Warehouse',
            'code': 'TecStore',
        })
        cls.parent_location = cls.env['stock.location'].create({
            'name': 'Parent',
        })
        cls.location_table_one = cls.env['stock.location'].create({
            'name': 'Mesa 1',
            'is_count_location': True,
            'location_id': cls.parent_location.id
        })
        cls.location_table_two = cls.env['stock.location'].create({
            'name': 'Mesa 2',
            'is_count_location': True,
            'location_id': cls.parent_location.id
        })
        cls.product_standard_one = cls.env['product.product'].create({
            'name': 'TecStore Product',
            'type': 'product',
        })
        cls.product_standard_two = cls.env['product.product'].create({
            'name': 'TecStore Product 2',
            'type': 'product'
        })
        cls.product_lot = cls.env['product.product'].create({
            'name': 'TecStore Lot Product',
            'type': 'product',
            'tracking': 'lot',
        })
        cls.lot_one = cls.env['stock.lot'].create({
            'name': 'TL-0001',
            'product_id': cls.product_lot.id,
        })
        cls.lot_two = cls.env['stock.lot'].create({
            'name': 'TL-0002',
            'product_id': cls.product_lot.id,
        })
        cls.quant_ids = cls.env['stock.quant'].create([{
            'product_id': cls.product_standard_one.id,  # xxx
            'location_id': cls.location_table_one.id,
            'lot_id': False,
            'inventory_quantity': 100.0,
            'inventory_quantity_set': True,
        }, {
            'product_id': cls.product_standard_one.id,  # xxx
            'location_id': cls.location_table_two.id,
            'lot_id': False,
            'inventory_quantity': 100.0,
            'inventory_quantity_set': True,
        }, {
            'product_id': cls.product_lot.id,  # yyy
            'location_id': cls.location_table_one.id,
            'lot_id': cls.lot_one.id,  # aaa
            'inventory_quantity': 100.0,
            'inventory_quantity_set': True,
        },
            {
            'product_id': cls.product_lot.id,  # yyy
            'location_id': cls.location_table_two.id,
            'lot_id': cls.lot_one.id,  # aaa
            'inventory_quantity': 100.0,
            'inventory_quantity_set': True,
        },
            {
            'product_id': cls.product_lot.id,  # yyy
            'location_id': cls.location_table_one.id,
            'lot_id': cls.lot_two.id,  # bbb
            'inventory_quantity': 100.0,
            'inventory_quantity_set': True,
        },
            {
            'product_id': cls.product_standard_two.id,  # zzz
            'location_id': cls.location_table_one.id,
            'lot_id': False,
            'inventory_quantity': 100.0,
            'inventory_quantity_set': True,
        }])

    def test_apply_all(self):
        before_product_standard = self.env['stock.quant'].search([('location_id', '=', self.parent_location.id),
                                                                  ('product_id', '=', self.product_standard_one.id)])
        before_product_lot_one = self.env['stock.quant'].search([('location_id', '=', self.parent_location.id),
                                                                 ('product_id', '=', self.product_lot.id),
                                                                 ('lot_id', '=', self.lot_one.id)])
        before_product_lot_two = self.env['stock.quant'].search([('location_id', '=', self.parent_location.id),
                                                                 ('product_id', '=', self.product_lot.id),
                                                                 ('lot_id', '=', self.lot_two.id)])
        before_product_standard_two = self.env['stock.quant'].search([('location_id', '=', self.parent_location.id),
                                                                      ('product_id', '=', self.product_standard_two.id)])

        self.quant_ids._apply_inventory()

        after_product_standard = self.env['stock.quant'].search([('location_id', '=', self.parent_location.id),
                                                                 ('product_id', '=', self.product_standard_one.id)])
        after_product_lot_one = self.env['stock.quant'].search([('location_id', '=', self.parent_location.id),
                                                               ('product_id', '=', self.product_lot.id),
                                                               ('lot_id', '=', self.lot_one.id)])
        after_product_lot_two = self.env['stock.quant'].search([('location_id', '=', self.parent_location.id),
                                                               ('product_id', '=', self.product_lot.id),
                                                               ('lot_id', '=', self.lot_two.id)])
        after_product_standard_two = self.env['stock.quant'].search([('location_id', '=', self.parent_location.id),
                                                                     ('product_id', '=', self.product_standard_two.id)])

        for quant in self.quant_ids:
            self.assertEqual(quant.quantity, 0.0, "past quant quantity is correct")
            self.assertEqual(quant.inventory_quantity, 0.0, "past quant inventory_quantity is correct")
            self.assertEqual(quant.inventory_diff_quantity, 0.0, "past quant inventory_quantity is correct")

        self.assertEqual(len(before_product_standard) + 1, len(after_product_standard),
                         "New line for Tec Store Product created")
        self.assertEqual(after_product_standard.inventory_quantity,
                         200.0, "Tec Store Product inventory quantity correct")
        self.assertEqual(after_product_standard.inventory_diff_quantity,
                         200.0, "Tec Store Product difference quantity correct")

        self.assertEqual(len(before_product_lot_one) + 1, len(after_product_lot_one),
                         "New line for Tec Store Lot Product created")
        self.assertEqual(after_product_lot_one.lot_id.name,
                         "TL-0001", "Tec Store Product Lot name correct")
        self.assertEqual(after_product_lot_one.inventory_quantity, 200.0,
                         "Tec Store Product Lot inventory quantity correct")
        self.assertEqual(after_product_lot_one.inventory_diff_quantity,
                         200.0, "Tec Store Product Lot difference quantity correct")

        self.assertEqual(len(before_product_lot_two) + 1, len(after_product_lot_two),
                         "New line for Tec Store Lot 2 Product created")
        self.assertEqual(after_product_lot_two.lot_id.name,
                         "TL-0002", "Tec Store Product Lot 2 name correct")
        self.assertEqual(after_product_lot_two.inventory_quantity, 100.0,
                         "Tec Store Product Lot 2 inventory quantity correct")
        self.assertEqual(after_product_lot_two.inventory_diff_quantity,
                         100.0, "Tec Store Product Lot 2 difference quantity correct")

        self.assertEqual(len(before_product_standard_two) + 1, len(after_product_standard_two),
                         "New line for Tec Store Product 2 created")
        self.assertEqual(after_product_standard_two.inventory_quantity, 100.0,
                         "Tec Store Product 2 inventory quantity correct")
        self.assertEqual(after_product_standard_two.inventory_diff_quantity,
                         100.0, "Tec Store Product 2 difference quantity correct")
