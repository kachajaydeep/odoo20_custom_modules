# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api


class PosConfig(models.Model):
    _inherit = "pos.config"

    apply_commission = fields.Boolean()
    commission_employee_ids = fields.Many2many("hr.employee")
