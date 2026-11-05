# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import _, api, models


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'
    
    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'hesabe':
            return res

        return self.provider_id._get_hesabe_form_generate_values(
            self.provider_id,self.currency_id,self.partner_id,self.reference,self.provider_code,self.amount
        )

    @api.model
    def _extract_reference(self, provider_code, payment_data):
        """Override of `payment` to extract the reference from the Hesabe data."""
        if provider_code != 'hesabe':
            return super()._extract_reference(provider_code, payment_data)
        return payment_data.get('response').get('orderReferenceNumber')

    def _extract_amount_data(self, payment_data):
        """Override of `payment` to extract the amount and currency from the payment data."""
        if self.provider_code != 'hesabe':
            return super()._extract_amount_data(payment_data)

        amount = float(payment_data.get('response', {}).get('amount', 0.00))
        return {
            'amount': amount,
            'currency_code': payment_data.get('response', {}).get('currency', 'KWD'),
        }

    def _apply_updates(self, payment_data):
        """Override of `payment' to update the transaction based on the payment data."""
        if self.provider_code != 'hesabe':
            return super()._apply_updates(payment_data)

        self.provider_reference = payment_data.get('response').get('paymentId')

        status = payment_data.get('status')
        if status:
            self._set_done()
        else:
            self._set_canceled()
