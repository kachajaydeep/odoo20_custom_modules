# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, http
from odoo.http import request
from odoo.addons.hr_attendance.controllers.main import HrAttendance


class HrAttendanceInherit(HrAttendance):

    @staticmethod
    def _get_user_attendance_data(employee):
        result = super(HrAttendanceInherit, HrAttendanceInherit)._get_user_attendance_data(employee)
        result['break'] = employee.nf_break
        result['break_start'] = employee.break_start
        return result


class EmployeeDashboardController(http.Controller):

    @staticmethod
    def __nf_get_employee_dashboard_data(employee):
        response = {}
        if employee:
            response = {
                'id': employee.id,
                'nf_break': employee.nf_break,
                'break_start': employee.break_start,
            }
        return response

    @http.route(
        '/nf_employee_management/nf_get_employee_data',
        type='jsonrpc', 
        auth='user',
        readonly=True
    )
    def employee_attendence_data(self):
        employee = request.env.user.employee_id
        return self.__nf_get_employee_dashboard_data(employee)