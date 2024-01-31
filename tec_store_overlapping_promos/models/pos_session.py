from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _get_pos_ui_product_pricelist(self, params):
        pricelists = super()._get_pos_ui_product_pricelist(params)
        for pricelist in pricelists:
            pricelist['collaborator_list'] = True if pricelist['id'] == self.env.ref("tec_store_overlapping_promos.collaborator_list").id else False
        return pricelists
