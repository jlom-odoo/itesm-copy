{
    "name": "ITESM Stock",
    "summary": "Changes to replenishments and inventory count",
    "description": """
    - Create a new reordering rule upon product creation, with the product's internal_code as part of the reordering rule external id
    - Add Count Location boolean field in stock location
    - Show parent location in Inventory Adjustment view
    - Group by location and product and sum quantities of each group
    - Assign the new groups to the parent location
    - Only show routes with supplied warehouse equal to the location's warehouse
    - Add boolean in stock route model labelled backoffice route
    - Add backoffice group with all permissions
    - Add record rule to hide routes with backoffice route enabled except for users in the backoffice group

    - Developers: EUVM,COGS,IASE
    - Task IDs: 3470757,3513703,3470766
    """,
    "category": "Custom Development",
    "version": "1.0.0",
    "author": "Odoo, Inc",
    "website": "https://www.odoo.com/",
    "license": "OPL-1",
    "depends": [
        'stock'
    ],
    "data": [
        'security/reorder_rule_locations_groups.xml',
        'security/reorder_rule_locations_security.xml',
        'security/ir.model.access.csv',
        'views/stock_location_views.xml',
        'views/stock_quant_views.xml',
        'views/stock_route_views.xml',
        'views/stock_warehouse_views.xml',
    ],
    'post_init_hook': 'update_orderpoint_external_ids'
}
