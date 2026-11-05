# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class PaymentProvider(models.Model):
    """ Inherited class of payment provider to add myfatoorah functions"""
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('myfatoorah', "MyFatoorah")], ondelete={'myfatoorah': 'set default'})
    myfatoorah_api_token = fields.Char(string='API Token')

    @api.model
    def _get_payment_method_information(self):
        """ Override method to add MyFatoorah payment method information."""
        res = super()._get_payment_method_information()
        res['mfatoorah'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        return res

    def _myfatoorah_get_api_url(self):
        """ Return the API URL according to the provider state.
        Note: self.ensure_one()
        :return: The API URL
        :rtype: str
        """
        self.ensure_one()
        currency = self.main_currency_id.name
        if self.is_live == True:
            url = ''
            # Kuwait, Bahrain, Jordan, Oman
            if currency in ['KWD', 'BHD', 'JOD', 'OMR']:
                url = 'https://api.myfatoorah.com/'
            # UAE
            elif currency == 'AED':
                url = 'https://api-ae.myfatoorah.com/'
            # Saudi Arabia
            elif currency == 'SAR':
                url = 'https://api-sa.myfatoorah.com/'
            # Qatar
            elif currency == 'QAR':
                url = 'https://api-qa.myfatoorah.com/'
            # Egypt
            elif currency == 'EGP':
                url = 'https://api-eg.myfatoorah.com/'
            else:
                raise ValidationError(_(f"Currency {currency} is not supported!"))
            return url
        else:
            return 'https://apitest.myfatoorah.com/'

    # @api.onchange('state')
    # def _onchange_state_switch_is_published(self):
    #     """ Automatically publish or unpublish the provider depending on its state.
    #     :return: None
    #     """
    #     self.is_published = self.state != 'disabled'
    #     if self.state == 'test':
    #         self.myfatoorah_api_token = 'SK_KWT_vVZlnnAqu8jRByOWaRPNId4ShzEDNt256dvnjebuyzo52dXjAfRx2ixW5umjWSUx'
