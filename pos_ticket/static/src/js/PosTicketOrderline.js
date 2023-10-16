odoo.define('pos_ticket.PosTicketOrderline', function(require) {
    'use strict';
    const {Orderline} = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const PosTicketOrderline = (Orderline) => class PosTicketOrderline extends Orderline {
        export_for_printing() {
            const result = super.export_for_printing(...arguments);
            result.product_default_code = this.get_product().default_code;
            return result;
        }
    }
    Registries.Model.extend(Orderline, PosTicketOrderline);
});
