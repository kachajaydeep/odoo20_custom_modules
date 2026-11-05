# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api


class PosSession(models.Model):
    _inherit = "pos.session"

    @api.model
    def _load_pos_data_models(self, config):
        model = super()._load_pos_data_models(config)
        model += ["pos.commission.line", "pos.commission.rules", "hr.employee"]

        return model
