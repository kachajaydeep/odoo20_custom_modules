# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    nf_pos_display_weight = fields.Boolean(string="Display Weight", readonly=False)
    nf_pos_display_volume = fields.Boolean(string="Display Volume", readonly=False)
    nf_display_weight_in_Receipt = fields.Boolean(string="Display Weight in Receipt", readonly=False)
    nf_pos_display_volume_in_receipt = fields.Boolean(string="Display Volume in Receipt", readonly=False)