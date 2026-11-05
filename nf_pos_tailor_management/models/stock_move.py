# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = "stock.move"

    nf_tailor_order_id = fields.Many2one("nf.tailor.order", string="Tailor Order")
