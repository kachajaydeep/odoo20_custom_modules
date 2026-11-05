# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, api, _


class StockPicking(models.Model):
    _inherit = "stock.move.line"

    @api.onchange('qty_done')
    def nf_onchange_qty_done(self):
        for move_line in self:
            if move_line.picking_id.location_dest_id and move_line.picking_id.location_id:
                if move_line.product_id:
                    sourse_location_quant_id = move_line.location_id.quant_ids.search([('product_id', '=', move_line.product_id.id), ('location_id', '=', move_line.picking_id.location_id.id)])
                    dest_location_quant_id = move_line.location_id.quant_ids.search([('product_id', '=', move_line.product_id.id), ('location_id', '=', move_line.picking_id.location_dest_id.id)])
                    if sourse_location_quant_id:
                        for quant_id in sourse_location_quant_id:
                            if quant_id.quantity <= move_line.qty_done:
                                move_line.qty_done = 0.00
                                # raise UserError()
                                return {'warning': {'title': _('Transfer Error'), 'message':_("You don't have enough stock of this Product (%s) in %s Location. \n In Source Location = %d Quantity, \n In Destination Location = %d Quantity") % (move_line.product_id.name, move_line.location_id.name,quant_id.quantity ,dest_location_quant_id.quantity)}
                                }
                            
class StockPicking(models.Model):
    _inherit = "stock.move"

    @api.onchange('product_uom_qty')
    def nf_onchange_qty_done(self):
        for move_line in self:
            if move_line.picking_id.picking_type_id.default_location_src_id and move_line.picking_id.picking_type_id.default_location_dest_id:
                if move_line.picking_id.location_dest_id and move_line.picking_id.location_id:
                    if move_line.product_id:
                        sourse_location_quant_id = move_line.location_id.quant_ids.search([('product_id', '=', move_line.product_id.id), ('location_id', '=', move_line.picking_id.location_id.id)])
                        dest_location_quant_id = move_line.location_id.quant_ids.search([('product_id', '=', move_line.product_id.id), ('location_id', '=', move_line.picking_id.location_dest_id.id)])
                        if sourse_location_quant_id:
                            for quant_id in sourse_location_quant_id:
                                if quant_id.quantity <= move_line.product_uom_qty:
                                    move_line.product_uom_qty = 0.00
                                    # raise UserError()
                                    return {'warning': {'title': _('Transfer Error'), 'message':_("You don't have enough stock of this Product (%s) in %s Location. \n In Source Location = %d Quantity, \n In Destination Location = %d Quantity") % (move_line.product_id.name, move_line.location_id.name,quant_id.quantity ,dest_location_quant_id.quantity)}
                                    }
