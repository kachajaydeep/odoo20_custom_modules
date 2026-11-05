# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

import json
from odoo import models, fields, api, _
from werkzeug import urls
from odoo.exceptions import ValidationError

from odoo.addons.nf_payment_hesabe import const
from odoo.addons.nf_payment_hesabe.hesabecrypt import encrypt, decrypt
from odoo.addons.nf_payment_hesabe.utils import checkout


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'
  
    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        return res
         
    code = fields.Selection(selection_add=[('hesabe', 'Hesabe')], ondelete={'hesabe': 'set default'})
    merchant_code = fields.Char(string="Merchant Code", required_if_provider='hesabe')
    secret_key = fields.Char(string="Secret Key", required_if_provider='hesabe')
    access_code = fields.Char(string="Access Code", required_if_provider='hesabe')
    iv_key = fields.Char(string="IV Key", required_if_provider='hesabe')
    api_version = fields.Char(string="API Version", required_if_provider='hesabe', default='2.0')
    production_url = fields.Char(string="Production Url", required_if_provider='hesabe')
    sandbox_url = fields.Char(string="Sandbox Url", required_if_provider='hesabe')

    def _get_default_payment_method_codes(self):
        self.ensure_one()
        if self.code != 'hesabe':
            return super()._get_default_payment_method_codes()
        return const.DEFAULT_PAYMENT_METHOD_CODES

    def _get_hesabe_url(self, environment):
        self.ensure_one()
        hesabe_form_url = ''
        if environment == False:
            hesabe_form_url = self.sandbox_url
        elif environment == True:
            hesabe_form_url = self.production_url
        return {'hesabe_form_url': hesabe_form_url}
    
    def _get_hesabe_form_generate_values(self, acqid, currencyid, partnerid, referenceno, providr, amount):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_str('web.base.url')
        company = self.env['res.company'].search([('id', '=', self.env.company.id)], limit=1).sudo()
        
        payload = {
            "merchantCode": acqid.merchant_code,
            "currency": company.currency_id.name,
            "amount": amount,
            "responseUrl": urls.url_join(base_url, '/payment/hesabe/%s/return' % ('knet' if self.code == 'hesabe' else 'mpgs')),
            "paymentType":'0',
            "version": acqid.api_version,
            "orderReferenceNumber": referenceno,
            "failureUrl": urls.url_join(base_url, '/payment/hesabe/%s/fail' % ('knet' if self.code == 'hesabe' else 'mpgs')),
            "variable2": amount,
        }

        parse_payload = json.loads(json.dumps(payload))
        url = self._get_hesabe_url(self.is_live)['hesabe_form_url']

        if parse_payload['currency'] != "KWD":
            raise ValidationError(_("Invalid currency: Selected currency("+ parse_payload['currency'] +") Please change currency to Kuwaiti Dinar (KWD)"))
        else:
            encryptedText = encrypt(str(json.dumps(payload)), self.secret_key, self.iv_key)
            checkoutToken = checkout(encryptedText, url, self.access_code, 'production' if self.is_live else 'test')
            try:
                result = decrypt(checkoutToken, self.secret_key, self.iv_key)
                try:
                    if '"status":false' in result:
                        raise ValidationError(
                            _("Service Unavailable: We are sorry the service is not available for this account. Please contact the business team for further information.")
                        )
                    response = json.loads(result)
                    decryptToken = response['response']['data']
                    if decryptToken != '':
                        url = urls.url_join(url, "/payment?data=%s" % (decryptToken))
                    else:
                        url = "/shop"
                except:
                    raise ValidationError(_("An exception occurred"))

                vals = {'form_url': url}
                return vals
            except:
                if '"status":false' and '"code":501' in checkoutToken:
                    raise ValidationError(_("Invalid Merchant: This Merchant doesn't support this payment method! double check your Access key , secret key and IV Key"))
                elif '"status":false' and '"code":503' in checkoutToken:
                    raise ValidationError(_("Invalid Merchant Service"))
                elif '"status":false' and '"code":519' in checkoutToken:
                    raise ValidationError(_("Invalid currency, Please use the same currency which has been used while authorizing the transaction"))
                elif '"status":false' and '"code":422' in checkoutToken:
                    raise ValidationError(_("Invalid Input"))
                elif '"status":false' and '"code":0' in checkoutToken:
                    raise ValidationError(_("Invalid Response"))
                elif '"status":false' and '"code":500' in checkoutToken:
                    raise ValidationError(_("Invalid Token"))
                elif '"status":false' and '"code":504' in checkoutToken:
                    raise ValidationError(_("Invalid Merchant Login Credentials"))
                elif '"status":false' and '"code":505' in checkoutToken:
                    raise ValidationError(_("Invalid Payment Token"))
                elif '"status":false' and '"code":506' in checkoutToken:
                    raise ValidationError(_("Invalid Request Data"))
                elif '"status":false' and '"code":507' in checkoutToken:
                    raise ValidationError(_("Transaction Error"))
                else:
                    raise ValidationError(_("Something went Wrong Please make sure your input is correct"))
        return vals
