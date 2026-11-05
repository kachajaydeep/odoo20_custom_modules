# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    nf_enable_bag_charges = fields.Boolean(related='pos_config_id.nf_enable_bag_charges',string="Enable Bag Charges",readonly=False)
    nf_carry_bag_category_id = fields.Many2one('pos.category',related='pos_config_id.nf_carry_bag_category_id',string="Carry Bag Category",domain=[],readonly=False)