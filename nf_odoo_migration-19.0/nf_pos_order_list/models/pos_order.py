# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api

class PosClasss(models.Model):
    _inherit = 'pos.order'

    @api.model
    def _load_pos_data_domain(self, data, config):
        domain = super()._load_pos_data_domain(data, config)
        # domain = [condition for condition in domain if condition[0] not in ['state', 'session_id']]
        print('\n\n\n -----domain----->',domain)
        return domain