# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    nf_pos_display_weight = fields.Boolean(related='pos_config_id.nf_pos_display_weight', readonly=False)
    nf_pos_display_volume = fields.Boolean(related='pos_config_id.nf_pos_display_volume', readonly=False)
    nf_display_weight_in_Receipt = fields.Boolean(related='pos_config_id.nf_display_weight_in_Receipt', readonly=False)
    nf_pos_display_volume_in_receipt = fields.Boolean(related='pos_config_id.nf_pos_display_volume_in_receipt', readonly=False)