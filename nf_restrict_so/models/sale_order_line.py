# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, api, _

class StockPicking(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('product_uom_qty')
    def nf_onchange_qty_done(self):
        for line in self:
            if line.order_id.warehouse_id.lot_stock_id:
                if line.product_id:
                    location_quant_id = line.order_id.warehouse_id.lot_stock_id.quant_ids.search([('product_id', '=', line.product_id.id), ('location_id', '=', line.order_id.warehouse_id.lot_stock_id.id)])
                    for quant in location_quant_id:
                        if line.product_uom_qty > quant.quantity:
                            if not self.env.user.has_group('nf_restrict_so.group_allow_nagative_selling'):
                                line.product_uom_qty = 0.00
                            return {'warning': {'title': _('Low Stock'), 'message': _(''' You don't have enough stock ! \n (On Hand Stock = %d ) ''',quant.quantity )}}
                            