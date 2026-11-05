# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    _nf_enable_a4_size_receipt = fields.Boolean(
        string="Enable A4 size Receipt Print",
        related="pos_config_id._nf_enable_a4_size_receipt",
        readonly=False,
    )
    _nf_show_arabic_labels = fields.Boolean(
        string="Enable Arabic Labels",
        related="company_id._nf_show_arabic_labels",
        readonly=False,
    )
