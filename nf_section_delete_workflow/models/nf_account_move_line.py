# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api, _


class NfAccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    nf_section_name = fields.Char(
        string="Section Name",
        copy=False,
    )

    def _update_section_name(self):

        for move in self.mapped("move_id"):

            current_section = False

            lines = move.invoice_line_ids.sorted(key=lambda l: l.sequence or 0)

            for line in lines:

                if line.display_type == "line_section":
                    current_section = line.name
                    continue

                if line.display_type == "product":
                    line.with_context(
                        skip_section_update=True
                    ).write({
                        "nf_section_name": current_section or False
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
   