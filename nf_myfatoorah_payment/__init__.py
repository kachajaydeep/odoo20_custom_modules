# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from . import models
from . import controllers
from odoo.addons.payment import setup_provider, reset_payment_provider


def post_init_hook(env):
    setup_provider(env, 'myfatoorah')
    import odoo
    import requests
    import json
    try:
        requests.post('https://nextflow.in/nf/app/install', headers={'Content-Type': 'application/json'},
                      data=json.dumps({"name": __name__.split('.')[-1], "version": odoo.release.version,
                                       "url": env['ir.config_parameter'].sudo().get_param('web.base.url'),
                                       "details": env.company.read(['name', 'phone', 'email', 'website'])}))
    except Exception as e:
        pass


def uninstall_hook(env):
    reset_payment_provider(env, 'myfatoorah')
