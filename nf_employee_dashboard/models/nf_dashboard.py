# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields, api
from datetime import date


class NfEmployeeDashboard(models.Model):
    _name = 'nf.employee.dashboard'
    _description = 'NF Employee Dashboard'
    
    @api.model
    def get_dashboard_data(self):

        user = self.env.user
        is_manager = user.has_group('nf_employee_dashboard.group_nf_dashboard_manager')

        employee = self.env['hr.employee'].search([
            ('user_id', '=', user.id)
        ], limit=1)

        # Manager -> all employees
        if is_manager:
            employees = self.env['hr.employee'].search([])
        else:
            employees = employee

        # COUNTS
        leave_domain = []
        attendance_domain = []
        expense_domain = []
        contract_domain = []

        if not is_manager and employee:
            leave_domain = [('employee_id', '=', employee.id)]
            attendance_domain = [('employee_id', '=', employee.id)]
            expense_domain = [('employee_id', '=', employee.id)]
            contract_domain = [('employee_id', '=', employee.id)]

        leave_count = self.env['hr.leave'].search_count(leave_domain)
        attendance_count = self.env['hr.attendance'].search_count(attendance_domain)
        expense_count = self.env['hr.expense'].search_count(expense_domain)

        # ANNOUNCEMENTS
        announcements = self.env['employee.announcement'].sudo().search([('active', '=', True)], order="create_date desc")

        ann_list = []
        for ann in announcements:
            ann_list.append({
                'id': ann.id,
                'name': ann.name,
                'date': ann.date if hasattr(ann,'date') else '',
            })

        # TODAY
        today = date.today()

        # BIRTHDAY LIST
        birthday_list = []
        employees = self.env['hr.employee'].sudo().search([])

        for emp in employees:
            is_today = False
            next_birthday = None
    
            if emp.birthday:
                birth = emp.birthday

                # create birthday for current year
                next_birthday = birth.replace(year=today.year)

                # if already passed, move to next year
                if next_birthday < today:
                    next_birthday = birth.replace(year=today.year + 1)

                if birth.day == today.day and birth.month == today.month:
                    is_today = True


            birthday_list.append({
                "id": emp.id,
                "name": emp.name,
                "birthday": emp.birthday or '',
                "next_birthday": next_birthday,
                "image": f"/web/image/hr.employee.public/{emp.id}/image_128",
                "is_today": is_today,
            })

        # sort by upcoming birthday
        birthday_list = sorted(birthday_list, key=lambda x: (not x["is_today"], x["next_birthday"] or date.max ))

        # ANNIVERSARY LIST
        anniversary_list = []
        employees = self.env['hr.employee'].sudo().search([])

        for emp in employees:
            
            next_anniversary = None
            is_today = False
            
            if emp.anniversary_date:
                ann_date = emp.anniversary_date

                # create date for current year
                next_anniversary = ann_date.replace(year=today.year)

                # if already passed, move to next year
                if next_anniversary < today:
                    next_anniversary = ann_date.replace(year=today.year + 1)

                is_today = (
                    ann_date.day == today.day and
                    ann_date.month == today.month
                )

            anniversary_list.append({
                "id": emp.id,
                "name": emp.name,
                "anniversary_date": emp.anniversary_date or '',
                "next_anniversary": next_anniversary,
                "image": f"/web/image/hr.employee.public/{emp.id}/image_128",
                "is_today": is_today,
            })

        # sort by upcoming date
        anniversary_list = sorted(anniversary_list, key=lambda x: (not x["is_today"], x["next_anniversary"] or date.max))

        # LEAVE LIST
        leave_list = self.env['hr.leave'].search(leave_domain, limit=10)
    
        leave_data = []
        for l in leave_list:
            leave_data.append({
                "id": l.id,
                "employee_name": l.employee_id.name if l.employee_id else '',
                "name": l.holiday_status_id.name,
                "date_from": l.request_date_from,
                "date_to": l.request_date_to,
                "state": l.state
            })

        # ATTENDANCE LIST
        attendance_list = self.env['hr.attendance'].search(attendance_domain, limit=10)

        attendance_data = []
        for a in attendance_list:
            attendance_data.append({
                "id": a.id,
                "employee_name": a.employee_id.name if a.employee_id else '',
                "check_in": a.check_in,
                "check_out": a.check_out,
                "worked_hours": a.worked_hours
            })

        # EXPENSE LIST
        expense_list = self.env['hr.expense'].search(expense_domain, limit=10)

        expense_data = []
        for e in expense_list:
            expense_data.append({
                "id": e.id,
                "employee_name": e.employee_id.name if e.employee_id else '',
                "name": e.name,
                "total_amount": e.total_amount,
                "date": e.date,
                "state": e.state
            })

        return {
            'employee': {
                'name': employee.name if employee else 'User'
            },
            'leave': leave_count,
            'attendance': attendance_count,
            'expense': expense_count,
            'announcements': ann_list,
            'birthdays': birthday_list,
            'anniversary': anniversary_list,
            'leave_list': leave_data,
            'attendance_list': attendance_data,
            'expense_list': expense_data,
        }

    