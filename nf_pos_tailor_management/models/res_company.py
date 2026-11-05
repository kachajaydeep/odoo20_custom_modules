# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api, _


class ResCompany(models.Model):
    _name = "res.company"

    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        if self.nf_tailor_order_ids:
            fields += [
                "nf_picking_id",
                "nf_tailor_location_id",
                "nf_tailor_location_dest_id",
            ]

        return fields
