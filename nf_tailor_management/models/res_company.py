# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = "res.company"

    nf_picking_id = fields.Many2one('stock.picking.type', string="Picking type")
    nf_tailor_location_id = fields.Many2one('stock.location', 'Component Source Location')
    nf_tailor_location_dest_id = fields.Many2one('stock.location', 'Component Destination Location')
    

