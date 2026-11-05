# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 


from odoo import models, fields

class FleetRentalLocation(models.Model):
    _name='rental.location'

    # create field
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    address = fields.Text(string="Address", required=True)
    company_id = fields.Many2one('res.company', string="Company")
    user_id = fields.Many2one('res.users', string="Responsible Person", required=True)
    active = fields.Boolean(string="Active" , default=True)

   