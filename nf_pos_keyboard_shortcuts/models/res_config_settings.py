# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api #type: ignore

class PosConfig(models.TransientModel):
    _inherit = "res.config.settings"

    nf_enable_keyboard_shortcuts = fields.Boolean(
        related="pos_config_id.nf_enable_keyboard_shortcuts", 
        help="Enable keyboard shortcuts in POS.", 
        readonly=False
    )

    nf_shortcut_ids = fields.One2many(
        related="pos_config_id.nf_shortcut_ids",
        readonly=False,
    )