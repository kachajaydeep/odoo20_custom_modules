# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields


class HrExpense(models.Model):
    _inherit = "hr.expense"

    nf_pos_order_line_id = fields.Many2one("pos.commission.line", string="Commission")
