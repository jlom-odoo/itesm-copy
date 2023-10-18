odoo.define('pos_ticket.PosTicketOrder', function(require) {
    'use strict';
    const {Order} = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const PosTicketOrder = (Order) => class PosTicketOrder extends Order {
        export_for_printing() {
            const result = super.export_for_printing(...arguments);
            result.company.pos_ticket_qr_code = this.pos.company.pos_ticket_qr_code;
            result.company.pos_ticket_qr_code_url = 
                `/web/image?model=res.company&field=pos_ticket_qr_code&id=${this.pos.company.id}&unique=${this.pos.company.pos_ticket_qr_code}`;
            return result;
        }
    }
    Registries.Model.extend(Order, PosTicketOrder);
});
