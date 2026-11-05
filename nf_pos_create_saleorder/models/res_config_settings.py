# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    nf_enable_create_saleorder = fields.Boolean(
        related="pos_config_id.nf_enable_create_saleorder",
        readonly=False
    )
