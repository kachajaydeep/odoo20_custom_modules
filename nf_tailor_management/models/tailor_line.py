# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api
from collections import defaultdict

class TailorLine(models.Model):
    _name = 'nf.tailor.line'
    _description = 'Tailor Line'

    name = fields.Char(string="Line Name", required=True, readonly=True)
    order_id = fields.Many2one('nf.tailor.order', string="Tailor Order", required=True)
    product_id = fields.Many2one('product.product', string="Product")
    quantity = fields.Float(string="Quantity", default=1)
    uom_id = fields.Many2one('uom.uom', string="UoM", compute="_compute_uom")
    unit_price = fields.Float(string="Unit Price", compute="_compute_unit_price", store="True")
    company_id = fields.Many2one(related='order_id.company_id', store=True, index=True, precompute=True)

    @api.onchange('product_id')
    def _compute_uom(self):
        for record in self:
            if record.product_id:
                record.uom_id = record.product_id.uom_id
            else:
                record.uom_id = False

    @api.depends('product_id', 'quantity')
    def _compute_unit_price(self):
        for record in self:
            record.unit_price = 0
            if record.product_id:
                record.unit_price = record.product_id.lst_price * record.quantity
            else:
                record.unit_price =  0.00

    @api.model_create_multi
    def create(self, vals):
        # Set the name using the sequence if it's not already set
        for val in vals:
            if val.get('name', 'New') == 'New':
                val['name'] = self.env['ir.sequence'].next_by_code('nf.tailor.line.sequence') or 'New'
        return super().create(vals)
