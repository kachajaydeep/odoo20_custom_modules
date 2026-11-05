# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api


class PosSession(models.Model):
    _inherit = "pos.session"
    _description = "Pos Session"

    @api.model
    def _load_pos_data_models(self, config):
        models = super()._load_pos_data_models(config)
        models += [
            "nf.tailor.order",
            "nf.bom.component",
            "mrp.bom",
            "nf.mrp.bom",
            "mrp.bom.line",
            "nf.measurement",
            "nf.measurement.line",
            "nf.measurement.type",
            "nf.measurement.category",
            "nf.measurement.design",
            "nf.tailor.line",
            "nf.design.type",
            "nf.design.line",
        ]
        return models
