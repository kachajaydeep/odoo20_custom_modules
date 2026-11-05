# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import fields,models,api

class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    nf_enable_stock_request = fields.Boolean(string="Enable Stock Request From Pos")
    nf_is_inventory_admin = fields.Boolean(compute="_compute_nf_is_inventory_admin")

    @api.depends_context('uid')
    def _compute_nf_is_inventory_admin(self):
        for config in self:
            config.nf_is_inventory_admin = self.env.user.has_group('stock.group_stock_manager')