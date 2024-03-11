/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { ListController } from "@web/views/list/list_controller";

export class ItesmStockListController extends ListController {
  setup() {
    super.setup();
  }
  onClickCreate() {
    console.log("this.model.root.resModel", this.model.root.resModel)
    if (this.model.root.resModel !== "stock.warehouse.orderpoint")
      super.onClickCreate();
  }
}
