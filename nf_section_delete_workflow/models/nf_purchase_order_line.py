# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api, _

class NfPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    nf_section_name = fields.Char(
        string="Section Name",
        copy=False,
    )

    def _update_section_name(self):

        for order in self.mapped("order_id"):

            current_section = False

            lines = order.order_line.sorted(
                key=lambda l: (l.sequence or 0, l.id)
            )

            for line in lines:

                if line.display_type == "line_section":
                    current_section = line.name
                    continue

                if not line.display_type:
                    line.with_context(
                        skip_section_update=True
                    ).write({
                        "nf_section_name": current_section or False,
                    })

    @api.model_create_multi
    def create(self, vals_list):

        records = super().create(vals_list)

        records._update_section_name()

        return records

    def write(self, vals):

        res = super().write(vals)

        if not self.env.context.get("skip_section_update"):
            self._update_section_name()

        return res