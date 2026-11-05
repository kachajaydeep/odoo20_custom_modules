# -*- coding: utf-8 -*-
# Copyright (C) NextFlowIT

from odoo import models, fields

class PosConfig(models.Model):
    _inherit = "pos.config"

    nf_enable_lot_selection = fields.Boolean(string="Enable product lot selection")