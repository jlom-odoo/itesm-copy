from odoo import fields, models


class Location(models.Model):
    _inherit = 'stock.location'

    is_count_location = fields.Boolean('Is a Count location?')
