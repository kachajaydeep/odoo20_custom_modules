# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields

class PosConfig(models.Model):
    _inherit = "pos.config"

    nf_enbale_2x_print = fields.Boolean(string="Enable 2x Receipt Print")
    nf_copy_count = fields.Integer(string="Copies", default=1)