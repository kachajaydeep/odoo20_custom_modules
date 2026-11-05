# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields

class ResConfigSettingsInherited(models.TransientModel):
    _inherit = 'res.config.settings'
    
    nf_enable_direct_login = fields.Boolean(related='pos_config_id.nf_enable_direct_login', readonly=False)