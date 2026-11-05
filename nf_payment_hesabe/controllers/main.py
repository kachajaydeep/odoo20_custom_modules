# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

import pprint
import json
import werkzeug
from odoo import http
from odoo.http import request
from odoo.addons.nf_payment_hesabe.hesabecrypt import decrypt
from odoo.addons.payment.logging import get_payment_logger


_logger = get_payment_logger(__name__)


class HesabeController(http.Controller):

    @http.route([
        '/payment/hesabe/knet/return',
        '/payment/hesabe/knet/fail'
    ], type='http', auth='public', csrf=False, methods=['GET'], save_session=False)
    def hesabe_knet_return(self, **post):
        hesabe = request.env['payment.provider'].sudo().search([('code', '=', 'hesabe')], limit=1)
        data = decrypt(post['data'], hesabe.secret_key, hesabe.iv_key)
        response = json.loads(data)
        _logger.info("Handling redirection from HESABE with data:\n%s", pprint.pformat(response))
        if post:
            getTrans = request.env['payment.transaction'].sudo()._search_by_reference('hesabe', response)
            getTrans.with_context(payment_safe_write=True)._process(response)
        return werkzeug.utils.redirect('/payment/status')

    @http.route('/payment/hesabe', type='http', auth="public", csrf=False, methods=['POST'], save_session=False )
    def hesabe_payment(self, **post):
        return werkzeug.utils.redirect(post.get('form_url'))
