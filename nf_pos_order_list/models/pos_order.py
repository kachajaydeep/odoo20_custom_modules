# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models

class PosClasss(models.Model):
    _inherit = "pos.order"

    def nf_pos_get_all_orders(self, domain, limit, offset, config_id):
        config = self.env['pos.config'].browse(config_id).exists()
        if not config:
            return { 'ids': [], 'total': 0}
        
        base_domain = [('config_id', '=', config_id), ('state', '!=', 'draft')] + domain
        orders = self.search(base_domain, limit=limit, offset=offset, order='date_order desc')
        return {'ids': orders.ids, 'total': self.search_count(base_domain)}
