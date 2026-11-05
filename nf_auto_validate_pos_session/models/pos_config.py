# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields, api #type: ignore

class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    nf_enable_auto_session_validation = fields.Boolean(
        string="Enable Auto Session Validation",
        help="Automatically validate and close the POS session after a configured period."
    )  
    
    def _update_auto_validation_cron(self):
        cron = self.env.ref('nf_auto_validate_pos_session.ir_cron_pos_session',raise_if_not_found=False)
        if not cron:
            return
        enabled_configs = self.search_count([('nf_enable_auto_session_validation', '=', True)])
        cron.active = bool(enabled_configs)
        
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._update_auto_validation_cron()
        return records

    def write(self, vals):
        res = super().write(vals)
        self._update_auto_validation_cron()
        return res
        
    @api.constrains('nf_enable_auto_session_validation')
    def _check_auto_session_validation_time(self):
        for record in self:
            if not record.nf_enable_auto_session_validation:
                continue