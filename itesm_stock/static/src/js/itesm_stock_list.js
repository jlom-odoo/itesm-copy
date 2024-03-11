/** @odoo-module **/
import { ListController } from "@web/views/list/list_controller";

import {patch} from "@web/core/utils/patch";

patch(ListController.prototype, "itesm_stock_list_controller", {
  onClickCreate() {
    if (this.model.root.resModel !== "stock.warehouse.orderpoint")
      super.onClickCreate();
  }
})
