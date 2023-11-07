{
    "name": "Agile inventory count",
    "summary": "Allow inventory count by location",
    "description": """
Agile inventory count
=====================
- Add Count Location boolean field in stock location
- Show parent location in Inventory Adjustment view
- Group by location and product and sum quantities of each group
- Assign the new groups to the parent location

Developer: [cogs]
Task ID: 3513703
    """,
    "depends": ['stock'],
    "data": [
        'views/stock_location_views.xml',
        'views/stock_quant_views.xml',
    ],
    "version": "1.0.0",
    "category": "Custom Modules",
    "license": "OPL-1",
    "author": "Odoo Inc.",
    "maintainer": "Odoo Inc.",
    "website": "www.odoo.com",
}
