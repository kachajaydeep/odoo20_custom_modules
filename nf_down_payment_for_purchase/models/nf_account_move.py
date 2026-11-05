# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api, _

class NfAccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super().action_post()
        # After posting, update any linked PO down-payment line names
        for move in self:
            if move.move_type != 'in_invoice':
                continue
            dp_lines = move.invoice_line_ids.filtered('is_downpayment')
            for bill_line in dp_lines:
                po_line = bill_line.purchase_line_id
                if po_line and po_line.is_downpayment:
                    po_line.write({
                        'name': _('Down Payment: %s on %s') % (
                            move.name,
                            move.invoice_date or fields.Date.today(),
                        ),
                    })
        return res

    def button_cancel(self):
        res = super().button_cancel()
        # On cancel, update PO line name to show Cancelled
        for move in self:
            if move.move_type != 'in_invoice':
                continue
            dp_lines = move.invoice_line_ids.filtered('is_downpayment')
            for bill_line in dp_lines:
                po_line = bill_line.purchase_line_id
                if po_line and po_line.is_downpayment:
                    po_line.write({
                        'name': _('Down Payment: %s on %s') % (
                            _('Cancelled'),
                            move.invoice_date or fields.Date.today(),
                        ),
                    })
        return res