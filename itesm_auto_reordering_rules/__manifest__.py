{
    'name': 'ITESM Reordering Rules',
    'summary': 'Auto generate reordering rules with custom external Ids for products',
    'description': """
    - Create a new reordering rule upon product creation, with the product's internal_code as part of the reordering rule external id

    - Developer: EUVM
    - Task ID: 3470757
    """,
    'version': '1.0.0',
    'category': 'Custom Developments',
    'author': 'Odoo, Inc.',
    'maintainer': 'Odoo, Inc.',
    'website': 'www.odoo.com',
    'license': 'OPL-1',
    'depends': [
        'stock',
    ],
    'post_init_hook': 'update_orderpoint_external_ids'
}
