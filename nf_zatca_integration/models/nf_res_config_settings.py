# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    nf_zatca_api_mode = fields.Selection(related='company_id.nf_zatca_api_mode', readonly=False)

    @api.depends('company_id')
    def _compute_company_informations(self):
        super()._compute_company_informations()
        for record in self:
            if self.company_id.country_code == 'SA':
                record.company_informations += _(
                    '\nBuilding Number: %(building_number)s, Plot Identification: %(plot_identification)s\nNeighborhood: %(neighborhood)s',
                    building_number=self.company_id.nf_zatca_building_number,
                    plot_identification=self.company_id.nf_zatca_plot_identification,
                    neighborhood=self.company_id.street2,
                )
