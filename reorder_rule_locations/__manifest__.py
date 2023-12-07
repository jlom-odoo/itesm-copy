{
    "name": "Filter reordering rules by locations",
    "summary": "Show reordering rules with the same warehouse",
    "description": """
Filter reordering rules by locations
=====================
- Only show routes with supplied warehouse equal to the location's warehouse
- Add boolean in stock route model labelled backoffice route
- Add backoffice group with all permissions
- Add record rule to hide routes with backoffice route enabled except for users in the backoffice group

Developer: [iase]
Task ID: 3470766
    """,
    "depends": ['stock'],
    "data": [
        'security/reorder_rule_locations_groups.xml',
        'security/reorder_rule_locations_security.xml',
        'security/ir.model.access.csv',
        'views/stock_route_views.xml',
        'views/stock_warehouse_views.xml',
    ],
    "version": "1.0.0",
    "category": "Custom Modules",
    "license": "OPL-1",
    "author": "Odoo Inc.",
    "maintainer": "Odoo Inc.",
    "website": "www.odoo.com",
}
