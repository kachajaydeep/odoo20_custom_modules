# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields


class PosConfig(models.Model):
    _inherit = "pos.config"

    nf_restrict_discount = fields.Boolean(string="Enable Discount Limit from POS")
