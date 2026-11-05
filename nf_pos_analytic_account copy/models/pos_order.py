# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields,api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    nf_analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string="Analytic Account"
    )