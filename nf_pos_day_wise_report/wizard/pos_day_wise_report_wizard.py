# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api
from datetime import date


class POSDayWiseReportWizard(models.TransientModel):
    _name = "pos.day.wise.report.wizard"
    _description = "POS Day Wise Report Wizard"


    @api.depends("date")
    def _compute_pos_hr_installed(self):
        pos_configs = self.env["pos.config"].sudo().search([
            ("module_pos_hr", "=", True),
        ])

        for wizard in self:
            wizard.nf_pos_config_ids = pos_configs
            wizard.pos_hr_installed = bool(pos_configs)

    date = fields.Date(default=date.today())
    user_ids = fields.Many2many(comodel_name="res.users", string="Users")
    employee_ids = fields.Many2many(comodel_name="hr.employee", string="Employees")
    nf_pos_config_ids = fields.Many2many("pos.config", compute="_compute_pos_hr_installed")
    pos_hr_installed = fields.Boolean(string="HR Installed", compute="_compute_pos_hr_installed", store=True)

    def print_report(self):
        datas = self.read()[0]
        return self.env.ref("nf_pos_day_wise_report.nf_pos_day_wise_action").report_action([], data=datas)
