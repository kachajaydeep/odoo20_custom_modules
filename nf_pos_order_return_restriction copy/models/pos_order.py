# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields 
from datetime import datetime, timedelta

class PosOrder(models.Model):
    _inherit = "pos.order"

    return_exprired = fields.Boolean(string="expired", compute="_compute_expired")
    
    def _compute_expired(self):
        for order in self:
            if not order.config_id.nf_restrict_return_order:
                order.return_exprired = False
                continue
            else:
                expiration_day = order.config_id.nf_return_restrict_days
                today = datetime.today()
                expiration_date = today - timedelta(days=expiration_day)
        
                if expiration_date >= order.date_order:
                    order.return_exprired = True
                else: 
                    order.return_exprired = False