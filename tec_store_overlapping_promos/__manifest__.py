{
    'name': 'Tec Store: POS overlapping Rewards',
    'description': '''
        - This module limits the user to one reward per product. In the case of a user belonging to a list of collaborators, 
          the discount of the selected reward will be on the base price.
        - In the case of order discounts, the promotion is exclusive and no other reward can be applied.
        - Discounts on specific products will work as long as two rewards do not apply to the same product.
        - In the discount on the cheapest product. It will be checked that the product to which the discount 
          is applied does not have another discount.
        - The Buy X Get Y promotion will be prioritised and when used with any product it will automatically 
          be removed from any other promotion or discount calculation to ensure that the product only has this reward.
        Developer: [cmgv]
        Task ID: 3484968
    ''',
    'author': 'Odoo Development Services',
    'maintainer': 'Odoo Development Services',
    'website': 'https://www.odoo.com',
    'category': 'Custom Development',
    'data': ['data/pricelist_collaborator.xml'],
    'version': '1.0.0',
    'depends': ['pos_loyalty'],
    'assets': {
        'point_of_sale.assets': [
            'tec_store_overlapping_promos/static/src/js/**/*',
        ],
    },
    'license': 'OPL-1',
}
