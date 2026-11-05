# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models #type: ignore

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def nf_check_in_out_from_pos(self, geo_information=None, check_in=False, check_out=False):
        if check_in and self.attendance_state == 'checked_out':
            self.sudo()._attendance_action_change(geo_information)
        elif check_out:
            self.sudo()._attendance_action_change(geo_information)

        return True
    