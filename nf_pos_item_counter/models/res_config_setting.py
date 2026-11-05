# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields #type: ignore

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    nf_enable_line_count = fields.Boolean(related='pos_config_id.nf_enable_line_count', readonly=False)
    nf_enable_product_count = fields.Boolean(related='pos_config_id.nf_enable_product_count', readonly=False)