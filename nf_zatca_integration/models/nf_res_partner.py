# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    nf_zatca_building_number = fields.Char("Building Number")
    nf_zatca_plot_identification = fields.Char("Plot Identification")

    nf_zatca_additional_identification_scheme = fields.Selection([
        ('TIN', 'Tax Identification Number'),
        ('CRN', 'Commercial Registration Number'),
        ('MOM', 'Momra License'),
        ('MLS', 'MLSD License'),
        ('700', '700 Number'),
        ('SAG', 'Sagia License'),
        ('NAT', 'National ID'),
        ('GCC', 'GCC ID'),
        ('IQA', 'Iqama Number'),
        ('PAS', 'Passport ID'),
        ('OTH', 'Other ID')
    ], default="OTH", string="Identification Scheme", help="Additional Identification scheme for Seller/Buyer")

    nf_zatca_additional_identification_number = fields.Char("Identification Number (SA)",
                                                           help="Additional Identification Number for Seller/Buyer")

    @api.model
    def _commercial_fields(self):
        return super()._commercial_fields() + ['nf_zatca_building_number', 'nf_zatca_plot_identification',
                                               'nf_zatca_additional_identification_scheme',
                                               'nf_zatca_additional_identification_number']

    def _address_fields(self):
        return super()._address_fields() + ['nf_zatca_building_number', 'nf_zatca_plot_identification']
