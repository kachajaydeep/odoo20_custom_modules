# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api

class PosConfig(models.Model):
    _inherit = "pos.config"

    nf_enable_custom_variant = fields.Boolean(string='Enable Product Variants')
    