# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit="res.config.settings"

    nf_restrict_return_order = fields.Boolean(related="pos_config_id.nf_restrict_return_order", readonly=False)
    nf_return_restrict_days = fields.Integer(related="pos_config_id.nf_return_restrict_days", readonly=False)
    