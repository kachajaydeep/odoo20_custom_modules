# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, Command, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    tailor_order_id = fields.Many2one('nf.tailor.order', string="Tailor order")
    measurement_line_ids = fields.One2many(related='tailor_order_id.measurement_line_ids', copy=False)
    design_ids = fields.One2many(related='tailor_order_id.design_ids', copy=False)

    def _nf_prepare_picking_vals(self, partner, picking_type, location_id, location_dest_id):
        return {
            'partner_id': partner.id if partner else False,
            'user_id': False,
            'picking_type_id': picking_type.id,
            'move_type': 'direct',
            'location_id': location_id,
            'location_dest_id': location_dest_id,
            'state': 'draft',
            'tailor_order_id': self.tailor_order_id.id,
            'move_ids': [Command.create({
                'product_id': self.tailor_order_id.bom_id.product_id.id,
                'product_uom_qty': self.tailor_order_id.product_qty,
                'location_id':  self.company_id.nf_tailor_location_id.id,
                'location_dest_id': location_dest_id,
                # 'name': self.tailor_order_id.bom_id.product_id.display_name
            })]        
        }
    
    def action_confirm(self):
        if self.tailor_order_id:
            self.write(self._prepare_confirmation_values())
            positive_picking = self.env['stock.picking'].create(
                self._nf_prepare_picking_vals(self.partner_id, self.company_id.nf_picking_id, self.company_id.nf_tailor_location_id.id, self.company_id.nf_tailor_location_dest_id.id)
            )
            self.picking_ids = positive_picking.ids
            self.tailor_order_id.message_post(body=_("Sale Order Confirmed and delivery Created."))
            return True
        else:
            return super().action_confirm()
        
    
