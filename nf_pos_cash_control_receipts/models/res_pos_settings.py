# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api

class ResConfigPosInherit(models.TransientModel):
    _inherit = "res.config.settings"

    nf_enable_cash_in_ont_receipt = fields.Boolean(related="pos_config_id.nf_enable_cash_in_ont_receipt", readonly=False)
    nf_enable_cash_report = fields.Boolean(related="pos_config_id.nf_enable_cash_report", readonly=False)
    
    @api.onchange('nf_enable_cash_report')
    def _onchange_(self):
        if self.nf_enable_cash_report:
            self.nf_enable_cash_in_ont_receipt = True