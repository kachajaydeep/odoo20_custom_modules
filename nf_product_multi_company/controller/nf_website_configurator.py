# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.fields import Domain
from odoo.http import request

class WebsiteSaleConfigration(WebsiteSale):
    def _get_shop_domain(self, search, category, attribute_value_dict, search_in_description=True):
        domain = super()._get_shop_domain(search, category,attribute_value_dict,search_in_description)
        website_ids_domain = [
            '|',
            ('nf_website_ids','=',False),
            ('nf_website_ids','in',[request.website.id])
        ]
        
        return Domain.AND([domain,website_ids_domain])
    