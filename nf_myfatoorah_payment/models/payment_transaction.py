# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

import logging
from odoo import _, models, api
from odoo.exceptions import ValidationError
import requests
import json
from werkzeug import urls

from odoo.addons.nf_myfatoorah_payment.controllers.main import MyFatoorahController

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """ Function to fetch the values of the payment gateway"""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'myfatoorah':
            return res
        return self.send_payment_request()

    # @api.model
    # def _extract_reference(self, provider_code, payment_data):
    #     """Override of `payment` to extract the reference from the myfatoorah data."""
    #     if provider_code != 'myfatoorah':
    #         return super()._extract_reference(provider_code, payment_data)

    #     reference = ""
    #     if payment_data["Data"]["CustomerReference"]:
    #         reference = payment_data["Data"]["CustomerReference"]
    #     return reference
    
    @api.model
    def _extract_reference(self, provider_code, payment_data):
        if provider_code != 'myfatoorah':
            return super()._extract_reference(provider_code, payment_data)

        if not payment_data.get('IsSuccess'):
            return ''

        data = payment_data.get('Data') or {}

        reference = data.get('CustomerReference')

        if reference:
            return reference

        invoice = data.get('Invoice') or {}

        return invoice.get('Reference', '')

    def _extract_amount_data(self, payment_data):
        """Override of `payment` to extract the amount and currency from the payment data."""
        if self.provider_code != 'myfatoorah':
            return super()._extract_amount_data(payment_data)

        amount = float(payment_data["Data"]["InvoiceTransactions"][0]['PaidCurrencyValue'])
        currency = self.currency_id.name
        return {
            'amount': amount,
            'currency_code': currency,
        }

    def _apply_updates(self, payment_data):
        """Override of `payment' to update the transaction based on the payment data."""
        if self.provider_code != 'myfatoorah':
            return super()._apply_updates(payment_data)

        # Update the provider reference.
        self.provider_reference = payment_data["Data"]["InvoiceTransactions"][0]['PaymentId']

        if payment_data["Data"]["InvoiceTransactions"][0]['TransactionStatus'] == 'Failed':
            self._set_error(_("MyFatoorah: Transaction Failed %s.", payment_data["Data"]["InvoiceTransactions"][0]['Error']))
        elif not payment_data["IsSuccess"]:
            self._set_canceled()
            raise ValidationError("myfatoorah: " + _("Payment is not successful"))
        else:
            self._set_done()

    def send_payment_request(self):
        """Send payment information to MyFatoorah for processing."""
        base_url = self.provider_id.get_base_url()

        phone_code = self.partner_id.country_id.phone_code
        partner_phone = self.partner_phone
        if not partner_phone:
            raise ValueError("Please provide the phone number.")
        else:
            partner_phone = partner_phone.replace(str(phone_code), '')
            if partner_phone.startswith('+'):
                partner_phone = partner_phone[1:]
            elif not partner_phone:
                raise ValueError("Please provide the phone number in proper format")

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.provider_id.myfatoorah_api_token}',
        }
        data = {
            "NotificationOption": "ALL",
            "CustomerName": self.partner_name,
            "DisplayCurrencyIso": self.currency_id.name,
            "InvoiceValue": self.amount,
            "MobileCountryCode": phone_code,
            "CustomerMobile": partner_phone,
            "CustomerEmail": self.partner_email,
            "CallBackUrl": urls.url_join(base_url, MyFatoorahController._return_url),
            "ErrorUrl": urls.url_join(base_url, MyFatoorahController._error_url),
            "Language": "en",
            "CustomerReference": self.reference,
            "CustomerAddress": {
                "Address": f'{self.partner_address} ,{self.partner_city} '
                           f'{self.partner_zip} ,{self.partner_state_id.name} ,'
                           f'{self.partner_country_id.name}',
            },
        }
        response = requests.request("POST",
                                    f"{self.provider_id._myfatoorah_get_api_url()}v2/SendPayment",
                                    headers=headers, data=json.dumps(data))
        print("\n\n======================>>>>>>>>>>",data)
        print("\n\n============headers==========>>>>>>>>>>",headers)
        
        response_data = response.json()
        # if not response_data.get('IsSuccess'):
        #     validation_errors = response_data.get('ValidationErrors')
        #     if validation_errors:
        #         raise ValidationError(f"{validation_errors[0].get('Error')}")
        # if response_data.get('Data')['InvoiceURL']:
        #     data['InvoiceURL'] = response_data.get('Data')['InvoiceURL']
        # return {
        #     'api_url': urls.url_join(base_url, MyFatoorahController._response_url),
        #     'data': data,
        # }
        if not response_data.get('IsSuccess'):
            validation_errors = response_data.get('ValidationErrors')

            if validation_errors:
                error = validation_errors[0].get('Error')
            else:
                error = response_data.get('Message') or 'Unknown MyFatoorah API error'

            raise ValidationError(f"MyFatoorah payment failed: {error}")

        response_data_data = response_data.get('Data') or {}
        invoice_url = response_data_data.get('InvoiceURL')

        if not invoice_url:
            raise ValidationError(
                "MyFatoorah did not return an InvoiceURL. "
                f"Response: {response_data}"
            )

        data['InvoiceURL'] = invoice_url

        return {
            'api_url': urls.url_join(
                base_url,
                MyFatoorahController._response_url
            ),
            'data': data,
        }
