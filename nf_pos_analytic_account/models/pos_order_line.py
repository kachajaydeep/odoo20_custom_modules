# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields,api

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    nf_analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string="Analytic Account"
    )
    
    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ["nf_analytic_account_id"]
        return fields