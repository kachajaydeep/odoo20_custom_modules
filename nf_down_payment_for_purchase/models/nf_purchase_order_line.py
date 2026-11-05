# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api, _

class NfPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    amount_bill = fields.Monetary(
        string="Bill Amount",
        compute='_compute_amount_bill',
        currency_field='currency_id',
        store=True,
    )

    amount_to_bill = fields.Monetary(
        string="Un-invoiced Balance",
        compute='_compute_amount_to_bill',
        currency_field='currency_id',
        store=True,
    )

    qty_invoiced_posted = fields.Float(
        string="Invoiced Quantity (Posted)",
        compute='_compute_qty_invoiced_posted',
        digits='Product Unit of Measure',
        store=True,
    )
    
    is_downpayment = fields.Boolean(
        copy=False,
    )
    
    def copy_data(self, default=None):
        # Most dynamic — block at line level directly
        result = []
        for record in self:
            if record.is_downpayment:
                continue
            data = super(NfPurchaseOrderLine, record).copy_data(default=default)
            result.extend(data)
        return result
    
    @api.depends('invoice_lines', 'invoice_lines.price_total', 'invoice_lines.move_id.state', 'invoice_lines.move_id.payment_state')
    def _compute_amount_bill(self):
        for line in self:
            amount_bill = 0.0
            for inv_line in line.sudo()._get_invoice_lines():
                invoice = inv_line.move_id
                if invoice.state in ('draft', 'posted') or invoice.payment_state == 'invoicing_legacy':
                    invoice_date = invoice.invoice_date or fields.Date.context_today(line)
                    currency = inv_line.currency_id or line.currency_id
                    amount = currency._convert(
                        inv_line.price_total,
                        line.currency_id,
                        line.company_id,
                        invoice_date,
                    )
                    # Purchase = Bill (in_invoice) / Credit Note (in_refund)
                    if invoice.move_type == 'in_invoice':
                        amount_bill += amount        
                    elif invoice.move_type == 'in_refund':
                        amount_bill -= amount   
            line.amount_bill = amount_bill


    @api.depends('invoice_lines', 'invoice_lines.quantity', 'invoice_lines.move_id.state', 'invoice_lines.move_id.payment_state', 'invoice_lines.move_id.move_type')
    def _compute_qty_invoiced_posted(self):
        for line in self:
            qty_posted = 0.0
            for inv_line in line.sudo()._get_invoice_lines():
                invoice = inv_line.move_id
                if invoice.state not in ('cancel',):
                    # product_uom renamed to product_uom_id
                    inv_uom  = inv_line.product_uom_id
                    line_uom = line.uom_id  # Fix here

                    if inv_uom and line_uom:
                        qty_unsigned = inv_uom.sudo()._compute_quantity(
                            inv_line.quantity,
                            line_uom,
                        )
                    else:
                        qty_unsigned = inv_line.quantity

                    sign = getattr(invoice, 'direction_sign', 1)
                    qty_posted += qty_unsigned * -sign

            line.qty_invoiced_posted = qty_posted
            

    @api.depends('price_unit', 'discount', 'product_qty', 'qty_received', 'qty_invoiced_posted', 'is_downpayment', 'amount_bill', 'uom_id')
    def _compute_amount_to_bill(self):
        for line in self:
            if not line.is_downpayment and not line.product_qty:
                line.amount_to_bill = 0.0
                continue

            if line.is_downpayment:
                unbilled = line.price_unit - line.amount_bill
                line.amount_to_bill = max(unbilled, 0.0)
                continue

            qty_to_invoice = line.qty_received - line.qty_invoiced_posted

            if qty_to_invoice <= 0:
                line.amount_to_bill = 0.0
                continue

            discount_factor = 1.0 - (line.discount / 100.0) if line.discount else 1.0
            line.amount_to_bill = line.price_unit * discount_factor * qty_to_invoice
            