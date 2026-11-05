# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

import requests
import json
import logging
import pprint
from odoo import http
from odoo.http import request
import ast

_logger = logging.getLogger(__name__)


class MyFatoorahController(http.Controller):
    """ Instance for the myfatoorah controller """
    _response_url = '/payment/myfatoorah/response'
    _return_url = '/payment/myfatoorah/_return_url'
    _error_url = '/payment/myfatoorah/failed'

    @http.route(_return_url, type='http', auth='public', methods=['GET'])
    def myfatoorah_checkout(self, **data):
        """ Function to redirect to the payment checkout"""
        _logger.info("Received MyFatoorah return data:\n%s", pprint.pformat(data))
        # data = {'Id': '07076425112325074471', 'paymentId': '07076425112325074471'}

        response = self._myfatoorah_payment_status(data)
        tx_sudo = request.env['payment.transaction'].sudo()._search_by_reference('myfatoorah', response)
        if not tx_sudo:
            _logger.warning(
                "MyFatoorah: no transaction found matching data:\n%s",
                pprint.pformat(response)
            )
            return request.redirect('/payment/status')
        
        if tx_sudo.state in ('done', 'cancel', 'error'):
            _logger.info(
                "MyFatoorah: transaction %s already in state '%s', skipping reprocessing",
                tx_sudo.reference, tx_sudo.state
            )
            return request.redirect('/payment/status')

        try:
            # Use with_context to make this write tolerant of retries;
            # _process/_record itself handles locking the tx row safely.
            tx_sudo._record(response)
            # tx_sudo._process('myfatoorah', response)
            # tx_sudo.with_context(payment_safe_write=True)._process(response)    
        except Exception:
            _logger.exception(
                "MyFatoorah: error processing transaction %s", tx_sudo.reference
            )


        return request.redirect('/payment/status')    
    

    @http.route(_error_url, type='http', auth='user', website=True)
    def myfatoorah_payment_fail(self):
        """ Function to render the payment failed"""
        return request.render("nf_myfatoorah_payment.nf_myfatoorah_payment_failed")

    @http.route(_response_url, type='http', auth='public', website=True, methods=['POST'],
                csrf=False, save_session=False)
    def myfatoorah_payment_response(self, **data):
        """Function to get the payment response"""
        payment_data = ast.literal_eval(data["data"])
        vals = {
            'customer': payment_data["CustomerName"],
            'currency': payment_data["DisplayCurrencyIso"],
            'mobile': payment_data["CustomerMobile"],
            'invoice_amount': payment_data["InvoiceValue"],
            'address': payment_data["CustomerAddress"]["Address"],
            'payment_url': payment_data["InvoiceURL"],
        }
        return request.render("nf_myfatoorah_payment.nf_myfatoorah_payment_form", vals)

    @staticmethod
    def _myfatoorah_payment_status(data: dict):
        provider_id = request.env['payment.provider'].search([('code', '=', 'myfatoorah')], limit=1)

        payload = json.dumps({"Key": data.get('paymentId'), "KeyType": "paymentId"})
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {provider_id.myfatoorah_api_token}',
        }
        response = requests.request("POST", f"{provider_id._myfatoorah_get_api_url()}v2/GetPaymentStatus",
                                    headers=headers, data=payload)
        payment_data = response.json()
        _logger.info("MyFatoorah Payment Status data:\n%s", pprint.pformat(payment_data))

        return payment_data
        # {'Data': {'Comments': None,
        #           'CreatedDate': '2026-01-10T09:33:24.057',
        #           'CustomerEmail': 'pranav.nextflow@gmail.com',
        #           'CustomerMobile': '9658460629199',
        #           'CustomerName': 'Administrator',
        #           'CustomerReference': 'S00001',
        #           'DepositStatus': 'Not Deposited',
        #           'DueDeposit': 44.833,
        #           'ExpiryDate': 'January 13, 2026',
        #           'ExpiryTime': '09:33:24.057',
        #           'InvoiceDisplayValue': '45.000 KD',
        #           'InvoiceId': 6425237,
        #           'InvoiceItems': [],
        #           'InvoiceReference': '2026007767',
        #           'InvoiceStatus': 'Paid',
        #           'InvoiceTransactions': [{'AuthorizationId': '831000',
        #                                    'Card': {'Brand': 'Visa',
        #                                             'ExpiryMonth': '01',
        #                                             'ExpiryYear': '39',
        #                                             'FundingMethod': 'debit',
        #                                             'Issuer': 'The Co-Operative Bank '
        #                                                       'Plc',
        #                                             'IssuerCountry': 'GBR',
        #                                             'NameOnCard': 'dfdsfdf',
        #                                             'Number': '450875xxxxxx1019',
        #                                             'PanHash': 'b4eda25d8a64929c02240406fc5cdc5417e4d021e1d055e43edb61e8d4903cfa',
        #                                             'Token': ''},
        #                                    'CardNumber': '450875xxxxxx1019',
        #                                    'Country': 'India',
        #                                    'Currency': 'KD',
        #                                    'CustomerServiceCharge': '0.000',
        #                                    'DueValue': '45.000',
        #                                    'ECI': '05',
        #                                    'Error': None,
        #                                    'ErrorCode': '',
        #                                    'IpAddress': '103.178.154.248',
        #                                    'PaidCurrency': 'KD',
        #                                    'PaidCurrencyValue': '45.000',
        #                                    'PaymentGateway': 'VISA/MASTER',
        #                                    'PaymentId': '07076425237325078272',
        #                                    'ReferenceId': '7680268857246708804805',
        #                                    'TotalServiceCharge': '0.145',
        #                                    'TrackId': '10-01-2026_3250782',
        #                                    'TransactionDate': '2026-01-10T09:34:46.5533333',
        #                                    'TransactionId': '7680268857246708804805',
        #                                    'TransactionStatus': 'Succss',
        #                                    'TransationValue': '45.000',
        #                                    'VatAmount': '0.022'}],
        #           'InvoiceValue': 45.0,
        #           'Suppliers': [],
        #           'UserDefinedField': None},
        #  'IsSuccess': True,
        #  'Message': '',
        #  'ValidationErrors': None}


# @staticmethod
# def _myfatoorah_payment_status(data: dict):
#     provider_id = request.env['payment.provider'].sudo().search(
#         [('code', '=', 'myfatoorah')],
#         limit=1,
#     )

#     payment_id = data.get('paymentId') or data.get('Id')

#     if not payment_id:
#         _logger.error(
#             "MyFatoorah callback did not contain paymentId: %s",
#             data,
#         )
#         return {
#             'IsSuccess': False,
#             'Message': 'Payment ID is missing.',
#         }

#     api_url = provider_id._myfatoorah_get_api_url().rstrip('/')

#     url = f"{api_url}/v3/payments/{payment_id}"

#     headers = {
#         'Accept': 'application/json',
#         'Authorization': f'Bearer {provider_id.myfatoorah_api_token}',
#     }

#     _logger.info(
#         "Checking MyFatoorah payment. URL: %s, Payment ID: %s",
#         url,
#         payment_id,
#     )

#     try:
#         response = requests.get(
#             url,
#             headers=headers,
#             timeout=30,
#         )

#         _logger.info(
#             "MyFatoorah HTTP status: %s",
#             response.status_code,
#         )

#         _logger.info(
#             "MyFatoorah response: %s",
#             response.text,
#         )

#         response.raise_for_status()

#         payment_data = response.json()

#     except requests.RequestException as e:
#         _logger.exception(
#             "MyFatoorah payment status request failed: %s",
#             e,
#         )

#         return {
#             'IsSuccess': False,
#             'Message': str(e),
#         }

#     except ValueError:
#         _logger.exception(
#             "Invalid JSON returned by MyFatoorah: %s",
#             response.text,
#         )

#         return {
#             'IsSuccess': False,
#             'Message': 'Invalid response from MyFatoorah.',
#         }

#     _logger.info(
#         "MyFatoorah Payment Status data:\n%s",
#         pprint.pformat(payment_data),
#     )

#     return payment_data