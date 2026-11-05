# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, Command

class MrpProduction(models.Model):
    _inherit = "mrp.production"

    tailor_order_id = fields.Many2one('nf.tailor.order', string="Tailor order")
    measurement_line_ids = fields.One2many(related='tailor_order_id.measurement_line_ids', copy=False)
    design_ids = fields.One2many(related='tailor_order_id.design_ids', copy=False)
