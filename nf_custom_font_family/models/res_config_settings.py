# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    nf_is_custom_font = fields.Boolean(string="Is Custom Fonts",config_parameter='nf_custom_font_family.nf_is_custom_font',readonly=False)
    
    nf_font_family = fields.Selection([
        ('montserrat', "Montserrat"),
        ('open_Sans', "Open Sans"),
        ('raleway', "Raleway"),
        ('oswald', "Oswald"),
        ('custom',"Custom")
    ], string='Global Font Family', default='montserrat', 
       config_parameter='nf_custom_font_family.nf_font_family', readonly=False)

    nf_text = fields.Char(string="Custom Font",config_parameter="nf_custom_font_family.nf_text",readonly=False)