# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 


from odoo import models, fields, api

class FleetRentLine(models.Model):
    _name='fleet.rent.line'
    _rec_name = 'contract_id'


    #create fields
    contract_id = fields.Many2one('fleet.rent', string="Rent",required=True )
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle" ,required=True) 
    duration_value = fields.Float(related='contract_id.duration', string="Duration") 
    rate = fields.Float(string="Rate")
    subtotal = fields.Float(compute="compute_fleet_rent_line_tax_total", string="Amount" ,store=True)
    currency_id = fields.Many2one('res.currency', related="contract_id.currency_id", ondelete='restrict')
    taxes_id = fields.Many2many('account.tax', string="Taxes")
    tax_total = fields.Float(compute="compute_fleet_rent_line_tax_total", string="Tax total", store=True)
    total_amount = fields.Float(compute="compute_fleet_rent_line_tax_total", string="Tax Incl.", store=True)
    partner_id = fields.Many2one(related='contract_id.partner_id', string="Customer" )
    start_date = fields.Datetime(related='contract_id.start_date', string="Start")
    end_date = fields.Datetime(related='contract_id.end_date', string="End")

    # compute taxes total
    @api.depends('duration_value','rate','taxes_id')
    def compute_fleet_rent_line_tax_total(self):
        self.tax_total = 0.0
        self.total_amount =0.0
        self.subtotal = 0.0
        for line in self:
            tax_res = line.taxes_id.compute_all(line.rate, line.currency_id, quantity = line.duration_value)
            total_included = tax_res['total_included']
            total_excluded = tax_res['total_excluded']
            taxes_calculation = total_included - total_excluded
            line.tax_total = taxes_calculation
            line.total_amount = total_included
            line.subtotal = total_excluded

    # onchange vehicle_id 
    @api.onchange('vehicle_id')
    def onchange_fleet_vehicle_rate(self):
        for line in self:
            if line.contract_id.rent_type == 'hourly' :
                line.rate = line.vehicle_id.default_rate_hourly

            elif line.contract_id.rent_type == 'daily' :
                line.rate = line.vehicle_id.default_rate_daily

            elif line.contract_id.rent_type == 'monthly' :
                line.rate = line.vehicle_id.default_rate_mothly
