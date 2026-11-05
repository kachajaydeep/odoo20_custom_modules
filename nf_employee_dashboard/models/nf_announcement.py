# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields, api
from datetime import date


class NfAnnouncement(models.Model):
    _name = 'employee.announcement'
    _description = 'NF Company Announcement'
    _order = 'name'

    name = fields.Char(string='Announcement', required=True, tracking=True)
    date = fields.Date(string='Date', required=True)
    sequence = fields.Integer(string='Sequence')    
    active = fields.Boolean(string="Active", default=True)
    