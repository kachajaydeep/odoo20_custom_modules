# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    nf_enbale_check_in_out = fields.Boolean(string="Enable Check in / Check out from POS")
