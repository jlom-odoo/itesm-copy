/** @odoo-module **/

import PosComponent from "point_of_sale.PosComponent";
import ProductScreen from "point_of_sale.ProductScreen";
import Registries from "point_of_sale.Registries";
import { useListener } from "@web/core/utils/hooks";
import { _t } from "web.core";

export class RewardAmountButton extends PosComponent {
  setup() {
    super.setup();
    useListener("click", this.onClick);
  }

  async onClick() {
    const { confirmed, payload: amount } = await this.showPopup(
      "TextInputPopup",
      {
        title: _t("Enter Reward Amount"),
        startingValue: "",
        placeholder: _t("Amount"),
      }
    );
    let order = this.env.pos.get_order();
    if (confirmed && amount && amount > 0) {
      order.amount = -amount;
      for (let line of order.get_orderlines()) {
        if (line.is_reward_line) {
          line.price = -amount;
          line.points_cost = amount;
        }
      }
    } else {
      order.amount = 0;
      return "Amount is not valid";
    }
    return true;
  }
}

RewardAmountButton.template = "RewardAmountButton";

ProductScreen.addControlButton({
  component: RewardAmountButton,
});

Registries.Component.add(RewardAmountButton);
