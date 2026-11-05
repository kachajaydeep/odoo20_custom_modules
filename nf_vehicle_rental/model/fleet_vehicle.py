# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 


from odoo import models, fields, api

class FleetVehicle(models.Model):
    _inherit='fleet.vehicle'

    def _get_default_product(self):
        return self.env.ref('nf_vehicle_rental.product_product_vehicle', raise_if_not_found=False)

    status = fields.Selection([('available_to_rent',"Available to Rent"), 
                               ('in_use',"In Use"),
                               ('maintenance',"Maintenance"),
                               ('reserved',"Reserved")],default="available_to_rent" ,string="Status",readonly=True)
    is_rental_vehicle = fields.Boolean(string="Rental Vehicle")
    default_rate_hourly = fields.Float(string="Rate Hourly")
    default_rate_daily = fields.Float(string="Rate Daily")
    default_rate_mothly= fields.Float(string="Rate Monthly")
    location_id = fields.Many2one('rental.location', string="Location")
    vehicle_product_id = fields.Many2one('product.product',string="Rent Product",
                                         default=_get_default_product)
