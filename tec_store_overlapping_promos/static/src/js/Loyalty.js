odoo.define("tec_store_overlapping_promos.TecStoreOverlappingRewards", function (require) {
            "use strict";

    const concurrency = require('web.concurrency');
    const { Order } = require("point_of_sale.models");
    const Registries = require("point_of_sale.Registries");
    const { round_decimals } = require ('web.utils');
    const dropPrevious = new concurrency.MutexedDropPrevious(); 


    const TecStoreOverlappingRewards = (Order) =>
    class extends Order {
      /**
       * @override
       */
      _getDiscountableOnOrder(reward) {
          let orderLines = this.get_orderlines()
          let existsPromo = orderLines.filter(line => line.assigned_promo)
          if (existsPromo.length && existsPromo.some(promo => promo.assigned_promo !== reward.id)) {
            return { discountable: 0, discountablePerTax: {} };
          }
          orderLines.map(line => {
            line = Object.assign(line, {price: line.product.lst_price, assigned_promo: reward.id})
          })
          return super._getDiscountableOnOrder(...arguments)      
      }
      /**
       * @override
       */
      _getDiscountableOnCheapest(reward) {
          const cheapestLine = this._getCheapestLine();
          if(cheapestLine && !cheapestLine.assigned_promo || cheapestLine.assigned_promo == reward.id) {
            cheapestLine.assigned_promo = reward.id
            cheapestLine.price = cheapestLine.product.lst_price
          } else {
            return {discountable: 0, discountablePerTax: {}};
          }
          return super._getDiscountableOnCheapest(...arguments)      
      }
      /**
       * @override
       */
      _getDiscountableOnSpecific(reward) {
          const applicableProducts = reward.all_discount_product_ids;
          const linesToDiscount = [];
          const discountLinesPerReward = {};
          const orderLines = this.get_orderlines();
          const remainingAmountPerLine = {};
          for (const line of orderLines) {
              if (!line.get_quantity() || !line.price) {
                  continue;
              }
              //START PATCH
              if(line.is_reward_line || line.assigned_promo && line.assigned_promo != reward.id) {
                  continue;
              }
              remainingAmountPerLine[line.cid] = this.pricelist.collaborator_list ? line.product.lst_price : line.get_price_with_tax();
              //END PATCH
              if (applicableProducts.has(line.get_product().id) ||
                  (line.reward_product_id && applicableProducts.has(line.reward_product_id))) {
                  linesToDiscount.push(line);
                  //START PATCH
                  line.assigned_promo = reward.id
                  //END PATCH
              } else if (line.reward_id) {
                  const lineReward = this.pos.reward_by_id[line.reward_id];
                  if (lineReward.id === reward.id) {
                      linesToDiscount.push(line);
                      //START PATCH
                      line.assigned_promo = reward.id
                      //END PATCH
                  }
                  if (!discountLinesPerReward[line.reward_identifier_code]) {
                      discountLinesPerReward[line.reward_identifier_code] = [];
                  }
                  discountLinesPerReward[line.reward_identifier_code].push(line);
              }
          }
          //START PATCH
          linesToDiscount.map(line => line.price = line.product.lst_price)
          //END PATCH
          let cheapestLine = false;
          for (const lines of Object.values(discountLinesPerReward)) {
              const lineReward = this.pos.reward_by_id[lines[0].reward_id];
              if (lineReward.reward_type !== 'discount') {
                  continue;
              }
              let discountedLines = orderLines;
              if (lineReward.discount_applicability === 'cheapest') {
                  cheapestLine = cheapestLine || this._getCheapestLine();
                  discountedLines = [cheapestLine];
              } else if (lineReward.discount_applicability === 'specific') {
                  discountedLines = this._getSpecificDiscountableLines(lineReward);
              }
              if (!discountedLines.length) {
                  continue;
              }
              const commonLines = linesToDiscount.filter((line) => discountedLines.includes(line));
              if (lineReward.discount_mode === 'percent') {
                  const discount = lineReward.discount / 100;
                  for (const line of discountedLines) {
                      if (line.reward_id) {
                          continue;
                      }
                      if (lineReward.discount_applicability === 'cheapest') {
                          remainingAmountPerLine[line.cid] *= (1 - (discount / line.get_quantity()))
                      } else {
                          remainingAmountPerLine[line.cid] *= (1 - discount);
                      }
                  }
              } else {
                  const nonCommonLines = discountedLines.filter((line) => !linesToDiscount.includes(line));
                  const discountedAmounts = lines.reduce((map, line) => {
                      map[line.get_taxes().map((t) => t.id)];
                      return map;
                  }, {});
                  const process = (line) => {
                      const key = line.get_taxes().map((t) => t.id);
                      if (!discountedAmounts[key] || line.reward_id) {
                          return;
                      }
                      const remaining = remainingAmountPerLine[line.cid];
                      const consumed = Math.min(remaining, discountedAmounts[key]);
                      discountedAmounts[key] -= consumed;
                      remainingAmountPerLine[line.cid] -= consumed;
                  }
                  nonCommonLines.forEach(process);
                  commonLines.forEach(process);
              }
          }
          let discountable = 0;
          const discountablePerTax = {};
          for (const line of linesToDiscount) {
            discountable += remainingAmountPerLine[line.cid];
              const taxKey = line.get_taxes().map((t) => t.id);
              if (!discountablePerTax[taxKey]) {
                  discountablePerTax[taxKey] = 0;
              }
              discountablePerTax[taxKey] += (line.get_base_price()) * (remainingAmountPerLine[line.cid] / line.get_price_with_tax());
          }
          return {discountable, discountablePerTax};
      }
      /**
       * @override
       */
      _getRewardLineValuesProduct(args) {
        const reward = args['reward'];
        const product = this.pos.db.get_product_by_id(args['product'] || reward.reward_product_ids[0]);
        const reward_orderlines = this.orderlines.filter(orderline => orderline.product.id == args['product'])
        reward_orderlines.forEach(line => {
          line = Object.assign(line, {price: line.product.lst_price, assigned_promo: args['reward'].id})
        })
        const productRewards = super._getRewardLineValuesProduct(...arguments)
        if (typeof(productRewards)==="object")
          productRewards.forEach(reward => reward.price = -round_decimals(product.get_price(this.pos.pricelists.find(item => item["id"] === 1), productRewards[0].quantity), this.pos.currency.decimal_places))
        return productRewards
      }  
      /**
       * @override
       */
      _updateRewards() {
        if (this.pos.programs.length === 0) {
          return;
        }
        dropPrevious.exec(() => {return this._updateLoyaltyPrograms().then(async () => {
          const claimableRewards = this.getClaimableRewards(false, false, true);
          //START PATCH        
          const potentialFreeProductRewards = this.getPotentialFreeProductRewards();
          const specificRewards = (reward, type) => reward.program_id.program_type !== 'ewallet' && reward.reward_type === type;  
          const discountRewards = claimableRewards.filter(({ reward }) => specificRewards(reward, 'discount'));
          const freeProductRewards = claimableRewards.filter(({ reward }) => specificRewards(reward, 'product'));
          const numOfRewards = discountRewards.length + freeProductRewards.length + potentialFreeProductRewards.length;
          //END PATCH
          let changed = false;
          for (const {coupon_id, reward} of claimableRewards) {
                //START PATCH
                  if (reward.program_id.rewards.length === 1 && !reward.program_id.is_nominative &&  (!this.pricelist.collaborator_list) && (numOfRewards==1) &&
                    (reward.reward_type !== 'product' || (reward.reward_type == 'product' && !reward.multi_product)))
                //END PATCH
                    {
                      this._applyReward(reward, coupon_id);
                      changed = true;
                    }
                  }
            if (changed) {
              await this._updateLoyaltyPrograms();
            }
            this._updateRewardLines();
          })}).catch(() => {/* catch the reject of dp when calling `add` to avoid unhandledrejection */});
      }
    };
    Registries.Model.extend(Order, TecStoreOverlappingRewards);
  });
