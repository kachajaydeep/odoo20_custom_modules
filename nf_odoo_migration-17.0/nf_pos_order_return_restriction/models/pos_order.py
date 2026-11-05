# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields 
from datetime import datetime, timedelta

class PosOrder(models.Model):
    _inherit = "pos.order"
    
    def _export_for_ui(self, order):
        res = super()._export_for_ui(order)
        
        if order.config_id.nf_restrict_return_order:
            expiration_day = order.config_id.nf_return_restrict_days
            today = datetime.today()
            expiration_date = today - timedelta(days=expiration_day)
            
            if expiration_date <= order.date_order:
                res['return_exprired'] = False
            else: 
                res['return_exprired'] = True

        return res