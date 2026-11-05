# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

SUPPORTED_CURRENCIES = {
    'OMR'
}

PROVIDER_ADDRESSES = {
    'production': 'https://checkout.thawani.om',
    'test': 'https://uatcheckout.thawani.om'
}

DEFAULT_PAYMENT_METHODS = [
    # Primary payment methods.
    'card',
    # Brand payment methods.
    'visa',
    'mastercard'
]
