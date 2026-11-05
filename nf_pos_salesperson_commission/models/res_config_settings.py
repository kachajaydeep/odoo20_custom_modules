# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    apply_commission = fields.Boolean(
        related="pos_config_id.apply_commission",
        readonly=False,
        string="Apply Commission",
    )

    commission_employee_ids = fields.Many2many(
        "hr.employee",
        related="pos_config_id.commission_employee_ids",
        readonly=False,
        string="Commission Employee",
    )
