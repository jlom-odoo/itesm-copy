{
    'name': 'POS Rewards',
    'summary': 'Let the user input the amount to pay with gift cards or eWallet.',
    'description': '''
        This module allows the user to input the amount to pay with gift cards or eWallet.
        In the standard, if the gift card covers all the amount, the order is validated automatically.
        If the gift card does not cover all the amount, the total available amount will be used. 
        This module lets you chose a lower amount to pay with the gift card.

        Developer: [gecm]
        Task ID: 3449159
        Link to task: https://www.odoo.com/web#id=3449159&menu_id=4720&cids=17&action=5050&model=project.task&view_type=form
    ''',
    'author': 'Odoo PS',
    'website': 'https://www.odoo.com',
    'category': 'Custom Development',
    'version': '1.0.0',
    'depends': ['point_of_sale', 'loyalty'],
    'assets': {
        'point_of_sale.assets': [
            'tec_store_POS_rewards/static/src/js/**/*',
            'tec_store_POS_rewards/static/src/xml/**/*',
        ],
    },
    'license': 'OPL-1',
}
