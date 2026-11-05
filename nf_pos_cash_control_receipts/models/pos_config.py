# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api

class PosConfig(models.Model):
    _inherit = "pos.config"

    nf_enable_cash_in_ont_receipt = fields.Boolean(string="Enable Cash In/Out Receipt")
    nf_enable_cash_report = fields.Boolean(string="Enable Total Cash In/Out Receipt")
    
    @api.onchange('nf_enable_cash_report')
    def _onchange_(self):
        if self.nf_enable_cash_report:
            self.nf_enable_cash_in_ont_receipt = True