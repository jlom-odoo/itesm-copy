/** @odoo-module **/

import { RewardButton } from "@pos_loyalty/js/ControlButtons/RewardButton";
import { patch } from "@web/core/utils/patch"
import { Gui } from 'point_of_sale.Gui';
import { _t } from "web.core";

patch(RewardButton.prototype, "tec_store_promos", {
    /**
     * @override
     */
    async onClick() {
        const rewards = this._getPotentialRewards();
        if (rewards.length === 0) {
            await this.showPopup('ErrorPopup', {
                title: this.env._t('No rewards available.'),
                body: this.env._t('There are no rewards claimable for this customer.')
            });
            return false;
        }
        let _onclick = this._super
        const reward_lst = rewards.map(reward => reward.reward.description).join(', ');
        if (this.env.pos.selectedOrder.pricelist.collaborator_list) {
            const { confirmed } = await Gui.showPopup('ConfirmPopup', {
                title: _t('Colaborators list'),
                body: _t('It seems that you are on the partner list, if you apply this promotion you will lose the 10% discount. \n Available rewards for this product: \n') + reward_lst,
            });
            if (confirmed){
                _onclick()
            }
            return;
        }
        this._super(); 
    }
})
