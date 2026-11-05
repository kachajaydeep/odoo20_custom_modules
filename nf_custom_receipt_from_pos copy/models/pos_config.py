# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    nf_custom_receipt_template = fields.Boolean(string="Enable Multi Receipt Design")
    nf_receipt_template_id = fields.Many2one("nf.receipt.template",string="Receipt Template")
    