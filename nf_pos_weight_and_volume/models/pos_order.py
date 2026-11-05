# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields

class PosOrder(models.Model):
    _inherit = "pos.order"

    nf_order_total_volume = fields.Float(string='Total Volume', default=0.0)
    nf_order_total_weight = fields.Float(string='Total weight', default=0.0)