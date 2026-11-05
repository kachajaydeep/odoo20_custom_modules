# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields,api

class PosSession(models.Model):
    _inherit='pos.session'
    
    nf_analytic_account_id = fields.Many2one('account.analytic.account',string="POS Analytic Accounting")
    
    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ['nf_analytic_account_id']
        return fields
    
    @api.model
    def _load_pos_data_models(self, config):
        models = super()._load_pos_data_models(config)
        models += ["account.analytic.account"]
        return models
    

    def close_session_from_ui(self, payment_method_closing={}):
        close_session = super().close_session_from_ui(payment_method_closing)
        analytic_enabled = self.env.user.has_group(
            'analytic.group_analytic_accounting'
        )
        for session in self:
            if analytic_enabled and session.config_id.nf_analytic_account_id and close_session:
                session.nf_analytic_account_id = session.config_id.nf_analytic_account_id
        return close_session