# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'
     
    def _default_analytic_group(self):
        return self.env.ref('analytic.group_analytic_accounting', raise_if_not_found=False)
    
    nf_analytic_account_id = fields.Many2one('account.analytic.account', string="POS Analytic Accounting")