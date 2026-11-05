# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

import logging
from odoo import models, api, fields    #type: ignore
from datetime import timedelta
_logger = logging.getLogger(__name__)

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    break_notification_sent = fields.Boolean(string="Break Notified", default=False)
    checkout_notification_sent = fields.Boolean(string="check_out Notified", default=False)

    @api.model
    def nf_cron_send_break_reminders(self):
        now = fields.Datetime.now()
        attendances = self.search([('check_in', '!=', False),('check_out', '=', False),('break_notification_sent', '=', False)])
        session_ids = self.env['pos.session'].search([('state', '=', 'opened')])
        for attendance in attendances:
            elapsed = now - attendance.check_in
            
            if timedelta(hours=3) <= elapsed < timedelta(hours=3, minutes=5):  # allow 5-min window
                for session in session_ids:
                    try:
                        session.config_id._notify("nf_break_time_notification", {"employee_id": attendance.employee_id.id})
                    except Exception:
                        _logger.exception(
                            "Failed sending break notification for employee %s",
                            attendance.employee_id.id,
                        )
                attendance.break_notification_sent = True

    @api.model
    def nf_cron_send_shift_end_reminders(self):
        now = fields.Datetime.now()
        attendances = self.search([('check_in', '!=', False),('check_out', '=', False),('checkout_notification_sent', '=', False)])
        session_ids = self.env['pos.session'].search([('state', '=', 'opened')])
        for attendance in attendances:
            elapsed = now - attendance.check_in
            
            if timedelta(hours=8) <= elapsed < timedelta(hours=8, minutes=5):  # allow 5-min window
                for session in session_ids:
                    try:
                        session.config_id._notify("nf_checkout_notification", {"employee_id": attendance.employee_id.id})
                    except Exception:
                        _logger.exception(
                            "Failed sending shft end notification for employee %s",
                            attendance.employee_id,
                        )
                attendance.checkout_notification_sent = True