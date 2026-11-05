# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields

class City(models.Model):
    _name = 'nf.cities'
    _description = 'City'

    name = fields.Char(string='City Name', required=True)
    state_id = fields.Many2one('res.country.state',string='State')
    country_id = fields.Many2one('res.country',string='Country')