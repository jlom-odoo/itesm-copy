{
    "name": "ITESM: POS custom ticket",
    "summary": "Addition of SKUs and QR to POS ticket",
    "description": """
    - Add a QR code at the end of the POS receipt ticket
    - Add the SKU (internal reference) of each product
      in the receipt ticket before its name

    - Developer: JLOM
    - Task ID: 3470758
    """,
    "category": "Custom Development",
    "version": "1.0.0",
    "author": "Odoo, Inc",
    "website": "https://www.odoo.com/",
    "license": "OPL-1",
    "depends": [
        "point_of_sale",
    ],
    "data": [
        "views/res_company_views_inherit.xml"
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_ticket/static/src/js/**/*",
            "pos_ticket/static/src/xml/**/*",
        ],
    },
}
