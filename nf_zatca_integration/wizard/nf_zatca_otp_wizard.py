# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, _, api
from odoo.exceptions import UserError


class ZATCAOtpWizard(models.TransientModel):
    _name = 'zatca.otp.wizard'
    _description = 'Request ZATCA OTP'

    nf_zatca_renewal = fields.Boolean("PCSID Renewal",
                                     help="Used to decide whether we should call the PCSID renewal API or the CCSID API",
                                     default=False)
    nf_zatca_otp = fields.Char("OTP", copy=False, help="OTP required to get a CCSID. Can only be acquired through "
                                                      "the Fatoora portal.")
    journal_id = fields.Many2one('account.journal', default=lambda self: self.env.context.get('active_id'), required=True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if self.env.company.nf_zatca_api_mode == 'sandbox':
            res['nf_zatca_otp'] = '123456' if self.nf_zatca_renewal else '123345'
        return res

    def validate(self):
        if not self.nf_zatca_otp:
            raise UserError(_("You need to provide an OTP to be able to request a CCSID"))
        if self.nf_zatca_renewal:
            return self.journal_id._nf_zatca_get_production_CSID(self.nf_zatca_otp)
        self.journal_id._nf_zatca_api_onboard_journal(self.nf_zatca_otp)
