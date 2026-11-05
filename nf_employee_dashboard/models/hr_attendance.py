# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields,models,api
import datetime

class HrAttendance(models.Model):
    _inherit = "hr.attendance"
    
    bye = fields.Boolean("Bye ?")
    

    def nf_break_end(self):   
        current_time =datetime.datetime.now()
        if self.bye:
            self.sudo().write({'bye':False})
            
        else:
            self.sudo().write({'bye':True})
        return True