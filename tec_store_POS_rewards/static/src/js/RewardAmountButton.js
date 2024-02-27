/** @odoo-module **/

import PosComponent from "point_of_sale.PosComponent";
import ProductScreen from "point_of_sale.ProductScreen";
import Registries from "point_of_sale.Registries";
import { Gui } from 'point_of_sale.Gui';
import { useListener } from "@web/core/utils/hooks";
import { _t } from "web.core";

export class RewardAmountButton extends PosComponent {
  setup() {
    super.setup();
    useListener("click", this.onClick);
  }

  async onClick() {
    let order = this.env.pos.get_order();
    if (!order || order.is_empty()) {
      order.amount = 0;
      Gui.showNotification(_t("Electronic wallets cannot be applied in empty orders."));
      return false;
    }
    const selectedOrderLine = order.get_selected_orderline();
    if (!selectedOrderLine || !selectedOrderLine.is_reward_line) {
      Gui.showNotification(_t("Selected order line is not an electronic wallet."));
      return false;
    }
    const { confirmed, payload: amount } = await this.showPopup(
      "TextInputPopup",
      {
        title: _t("Enter Reward Amount"),
        startingValue: "",
        placeholder: _t("Amount"),
      }
    );
    if (confirmed && amount && amount > 0) {
      order.curr_amount_by_id = order.curr_amount_by_id || {};
      order.curr_amount_by_id[ selectedOrderLine.coupon_id ] = -amount;
      selectedOrderLine.price = -amount;
      selectedOrderLine.points_cost = amount;
    } else {
      order.amount = 0;
      Gui.showNotification(_t("Amount is not valid"));
      return false;
    }
    return true;
  }
}

RewardAmountButton.template = "RewardAmountButton";

ProductScreen.addControlButton({
  component: RewardAmountButton,
});

Registries.Component.add(RewardAmountButton);
