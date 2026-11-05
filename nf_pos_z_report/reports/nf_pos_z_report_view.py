# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api


class PosReport(models.AbstractModel):
    _name = "report.nf_pos_z_report.z_reports_details"

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            "doc_ids": data["session_ids"],
            "doc_models": self.env["pos.session"],
            "data": data,
            "docs": self.env["pos.session"].browse(data["session_ids"]),
        }
