# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api

class ResCofigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    nf_enable_custom_variant = fields.Boolean(related='pos_config_id.nf_enable_custom_variant', readonly=False,string='Enable Product Variants')
