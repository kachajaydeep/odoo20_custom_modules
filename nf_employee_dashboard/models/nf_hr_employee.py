# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields, api
from datetime import date

class NfHrEmployee(models.Model):
    _inherit = 'hr.employee'

    anniversary_date = fields.Date(string="Anniversary Date")
    
    nf_break = fields.Boolean(string='Break')
    timer_break = fields.Boolean()
    break_start = fields.Datetime(string="Break Start")
    break_end = fields.Datetime(string="Break End")

    def nf_break_start(self):
        now = fields.Datetime.now()

        if self.sudo().nf_break:
            self.sudo().write({'nf_break': False, "break_start": False})
        else:
            self.sudo().write({'nf_break': True, "break_start": now})
    
        return True
    
    def nf_emp_checkOut(self):
        attendance = self.env['hr.attendance'].sudo().search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
        
        if attendance:
            attendance.sudo().write({
                "bye":not attendance.bye
            })

        return True

        