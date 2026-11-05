# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    nf_picking_id = fields.Many2one(related='company_id.nf_picking_id',readonly=False)
    nf_tailor_location_id = fields.Many2one(related='company_id.nf_tailor_location_id',readonly=False)
    nf_tailor_location_dest_id = fields.Many2one(related='company_id.nf_tailor_location_dest_id',readonly=False)

    @api.onchange('nf_picking_id')
    def onchange_field(self):
        self.nf_tailor_location_id = self.nf_picking_id.default_location_src_id.id
        self.nf_tailor_location_dest_id = self.nf_picking_id.default_location_dest_id.id
    