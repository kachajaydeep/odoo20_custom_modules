# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields

class PosOrder(models.Model):
    _inherit = "pos.order"

    nf_global_discoount = fields.Float(string="Global Discount")
    nf_discount_type = fields.Selection([('percentage','Percentage'),('amount','Amount')], default='percentage', string='Discount Type')