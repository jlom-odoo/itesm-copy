import base64
from odoo import fields, models, tools
from odoo.modules.module import get_resource_path


class ResCompany(models.Model):
    _inherit = 'res.company'

    def _get_default_pos_ticket_qr_code(self):
        img_path = get_resource_path('pos_ticket', 'static/img/default_pos_ticket_qr_code.png')
        img_file = tools.file_open(img_path, 'rb')
        return base64.b64encode(img_file.read())
    
    pos_ticket_qr_code = fields.Image(string='Company PoS QR', 
                                      help='This field holds the image used to display a QR Code in the PoS receipt ticket for a given company.', 
                                      default=_get_default_pos_ticket_qr_code)
