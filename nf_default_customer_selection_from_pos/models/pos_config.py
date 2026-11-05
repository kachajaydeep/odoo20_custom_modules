# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    nf_is_default_selection_customer = fields.Boolean(string="Enable Default Customer")
    nf_default_customer_id = fields.Many2one("res.partner",string="Default Customer Selection")