# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo  import models, fields

class NfResCompany(models.Model):
    _inherit = 'res.company'
    
    nf_product_brand_on_view_enable = fields.Boolean(string="Product Brand on Views")
    nf_product_brand_report_enable = fields.Boolean(string="Product Brand on Reports")