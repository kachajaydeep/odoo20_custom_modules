# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields

class PosConfig(models.Model):
    _inherit = "pos.config"

    nf_theme_setting_id = fields.Many2one("nf.pos.theme.settings", string="Theme")