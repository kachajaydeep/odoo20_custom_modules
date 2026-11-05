# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models #type: ignore

class StockPickingInherited(models.Model):
    _inherit = 'stock.picking'
    
    def _prepare_stock_move_vals(self, first_line, order_lines):
        vals = super()._prepare_stock_move_vals(first_line, order_lines)

        lines_with_uom = order_lines.filtered(lambda l: l.selected_uom_id)

        if not lines_with_uom:
            return vals

        stock_uom = first_line.product_id.uom_id

        # Lines without a selected UOM — already in stock UOM, take as-is
        lines_without_uom = order_lines - lines_with_uom
        qty_in_stock_uom = abs(sum(lines_without_uom.mapped('qty')))

        # Lines with selected UOM — convert each group by its UOM
        for line in lines_with_uom:
            qty_in_stock_uom += line.selected_uom_id._compute_quantity(
                abs(line.qty),
                stock_uom,
                rounding_method='HALF-UP'
            )

        vals.update({
            'uom_id': stock_uom.id,
            'product_uom_qty': qty_in_stock_uom,
        })

        return vals