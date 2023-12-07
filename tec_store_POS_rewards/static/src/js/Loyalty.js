odoo.define("tec_store_POS_rewards.TecStoreLoyalty", function (require) {
  "use strict";

  const { _t } = require("web.core");
  const { Gui } = require("point_of_sale.Gui");
  const { Order } = require("point_of_sale.models");
  const Registries = require("point_of_sale.Registries");

  const TecStoreLoyalty = (Order) =>
    class extends Order {
      async _activateCode(code) {
        if ((await this._inputAmount(code)) !== true) {
          return;
        }
        return super._activateCode(code);
      }

      async _inputAmount(code) {
        // Get the coupon's maximum discount amount
        const result = await this.pos.env.services.rpc({
          model: "loyalty.card",
          method: "search_read",
          kwargs: {
            domain: [["code", "=", code]],
            fields: ["id", "points", "code", "partner_id", "program_id"],
            limit: 1,
          },
        });
        const { confirmed, payload: amount } = await Gui.showPopup(
          "TextInputPopup",
          {
            title: _t("Enter Reward Amount"),
            startingValue: result[0].points,
            placeholder: _t("Amount"),
          }
        );
        if (confirmed && amount && amount > 0) {
          this.amount = -amount;
        } else {
          this.amount = 0;
          return _t("Amount is not valid");
        }
        return true;
      }

      _getRewardLineValuesDiscount(args) {
        const values = super._getRewardLineValuesDiscount(args);
        if (values && values[0]) {
          if (values[0].price && values[0].price < this.amount) {
            values[0].price = this.amount;
          }
          if (values[0].points_cost && values[0].points_cost > -this.amount) {
            values[0].points_cost = -this.amount;
          }
        }
        return values;
      }

      _createLineFromVals(vals) {
        const line = super._createLineFromVals(vals);
        const lines = this.get_orderlines();
        for (let i = 0; i < lines.length; i++) {
          if (lines[i].is_reward_line && lines[i].product === line.product) {
            this.remove_orderline(lines[i]);
          }
        }
        return line;
      }
    };
  Registries.Model.extend(Order, TecStoreLoyalty);
});
