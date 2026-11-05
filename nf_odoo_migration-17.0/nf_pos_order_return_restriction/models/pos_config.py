# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields 

class PosConfig(models.Model):
    _inherit = "pos.config"

    nf_restrict_return_order = fields.Boolean(string="Restrict to return")
    nf_return_restrict_days = fields.Integer(string="Return Policy Days", default=30)
