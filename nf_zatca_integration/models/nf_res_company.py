# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

import re
from odoo import models, fields, _
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = "res.company"

    arabic_name = fields.Char('Arabic Name')
    arabic_city = fields.Char('City Arabic Name')

    nf_zatca_private_key_id = fields.Many2one(string="ZATCA Private key",
        comodel_name='certificate.key', copy=False,
        domain=[('public', '=', False)],
        help="The private key used to generate the CSR and obtain certificates",)

    nf_zatca_api_mode = fields.Selection([
        ('sandbox', 'Sandbox'),
        ('preprod', 'Simulation (Pre-Production)'),
        ('prod', 'Production')],
        help="Specifies which API the system should use", required=True,
        default='sandbox', copy=False)

    nf_zatca_building_number = fields.Char(compute='_compute_address', inverse='_nf_zatca_inverse_building_number')
    nf_zatca_plot_identification = fields.Char(compute='_compute_address',
                                               inverse='_nf_zatca_inverse_plot_identification')

    nf_zatca_additional_identification_scheme = fields.Selection(
        related='partner_id.nf_zatca_additional_identification_scheme', readonly=False)
    nf_zatca_additional_identification_number = fields.Char(
        related='partner_id.nf_zatca_additional_identification_number', readonly=False)

    journal_ids = fields.One2many(
        comodel_name='account.journal', inverse_name='company_id', string="Zatca Onboarding Journals",
        domain=[('type', '=', 'sale')])

    def _get_company_root_delegated_field_names(self):
        return super()._get_company_root_delegated_field_names() + [
            'nf_zatca_api_mode',
            'nf_zatca_private_key_id',
        ]

    def write(self, vals):
        for company in self:
            if 'nf_zatca_api_mode' in vals:
                if company.nf_zatca_api_mode == 'prod' and vals['nf_zatca_api_mode'] != 'prod':
                    raise UserError(_("You cannot change the ZATCA Submission Mode once it has been set to Production"))
                journals = self.env['account.journal'].search(self.env['account.journal']._check_company_domain(company))
                journals._nf_zatca_reset_certificates()
                journals.nf_zatca_latest_submission_hash = False
        return super().write(vals)

    def _get_company_address_field_names(self):
        """ Override to add ZATCA specific address fields """
        return super()._get_company_address_field_names() + \
            ['nf_zatca_building_number', 'nf_zatca_plot_identification']

    def _nf_zatca_inverse_building_number(self):
        for company in self:
            company.partner_id.nf_zatca_building_number = company.nf_zatca_building_number

    def _nf_zatca_inverse_plot_identification(self):
        for company in self:
            company.partner_id.nf_zatca_plot_identification = company.nf_zatca_plot_identification

    def _nf_zatca_get_csr_invoice_type(self):
        return '1100'

    def _nf_zatca_check_organization_unit(self):
        """
            Check company Organization Unit according to ZATCA specifications
            Standards:
                BR-KSA-39
                BR-KSA-40
            See https://zatca.gov.sa/ar/RulesRegulations/Taxes/Documents/20210528_ZATCA_Electronic_Invoice_XML_Implementation_Standard_vShared.pdf
        """
        self.ensure_one()
        if not self.vat:
            return False
        return len(self.vat) == 15 and bool(re.match(r'^3\d{13}3$', self.vat))
