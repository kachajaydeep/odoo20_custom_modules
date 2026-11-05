# -*- coding: utf-8 -*-
# Copyright (C) NextFlowIT

from odoo import models, fields

class ResConfigPosInherit(models.TransientModel):
    _inherit = "res.config.settings"

    nf_enable_lot_selection = fields.Boolean(related="pos_config_id.nf_enable_lot_selection", readonly=False)