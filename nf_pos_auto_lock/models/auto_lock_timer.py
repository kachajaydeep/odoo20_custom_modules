# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields, api, exceptions #type: ignore

class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    nf_enable_auto_lock = fields.Boolean(
        string="Enable POS Auto Lock",
        help="Automatically lock the POS screen after a period of inactivity."
    )
    
    nf_auto_lock_timeout = fields.Integer(
        string="Lock Screen After (Seconds)",
        default=120,
        help="Number of seconds of inactivity before the POS screen is locked."
    )
    
    @api.constrains('nf_auto_lock_timeout', 'nf_enable_auto_lock')
    def _check_auto_lock_timeout(self):
        for record in self:
            if not record.nf_enable_auto_lock:
                continue
            if record.nf_auto_lock_timeout < 30:
                raise exceptions.ValidationError(
                    "Lock timeout must be at least 30 seconds."
                )
            if record.nf_auto_lock_timeout > 86400:
                raise exceptions.ValidationError(
                    "Lock timeout cannot exceed 86400 seconds (24 hours)."
                )