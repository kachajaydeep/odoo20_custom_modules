# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    nf_custom_receipt_template = fields.Boolean(related='pos_config_id.nf_custom_receipt_template',string="Enable Multi Receipt Design",readonly=False)
    nf_receipt_template_id = fields.Many2one("nf.receipt.template",related='pos_config_id.nf_receipt_template_id',string="Receipt Template",readonly=False)

