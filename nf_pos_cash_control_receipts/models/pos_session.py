# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models

class PosSesion(models.Model):
    _inherit = "pos.session"

    def _pos_data_process(self, loaded_data):
        super()._pos_data_process(loaded_data)
        if self.config_id.module_pos_hr:
            loaded_data["bank_statement_line_by_id"] = {
                bank["id"]: bank for bank in loaded_data["account.bank.statement.line"]
            }

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        if "account.bank.statement.line" not in result:
            result.append("account.bank.statement.line")
        return result

    def _loader_params_account_bank_statement_line(self):
        return {
            "search_params": {
                "domain": [("pos_session_id", "=", self.id)],
                "fields": [],
                "load": False,
            }
        }

    def _get_pos_ui_account_bank_statement_line(self, params):
        return self.env["account.bank.statement.line"].search_read(
            **params["search_params"]
        )