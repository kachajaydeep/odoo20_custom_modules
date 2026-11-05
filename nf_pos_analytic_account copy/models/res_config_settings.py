# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    nf_analytic_account_id = fields.Many2one('account.analytic.account',string="POS Analytic Accounting",related="pos_config_id.nf_analytic_account_id",readonly=False)