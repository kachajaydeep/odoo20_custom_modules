# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    nf_restrict_discount = fields.Boolean(
        string="Enable Discount Limit from POS",
        related="pos_config_id.nf_restrict_discount",
        readonly=False,
    )
