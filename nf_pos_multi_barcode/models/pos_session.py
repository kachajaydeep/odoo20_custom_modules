# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models

class PosSession(models.Model):
    _inherit = "pos.session"

    def _load_pos_data_models(self, config_id):
        models_to_load = super()._load_pos_data_models(config_id)
        if "nf.multi.barcode" not in models_to_load:
            models_to_load.append("nf.multi.barcode")
        return models_to_load