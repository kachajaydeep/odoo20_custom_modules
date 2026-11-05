# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models #type: ignore

class PosSession(models.Model):
    _inherit = "pos.session"

    def _cron_auto_validate_sessions(self):
        sessions = self.search([('state', '=', 'opened')])
        for session in sessions:
            config = session.config_id
            if not config.nf_enable_auto_session_validation:
                continue
            
            if session.config_id:
                session.name = f"{session.config_id.name} - {session.name}"

            if not session.start_at:
                continue

            try:
                session.close_session_from_ui()

            except Exception as error:
                print(error)