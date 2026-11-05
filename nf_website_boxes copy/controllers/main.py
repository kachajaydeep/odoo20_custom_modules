# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.


from odoo.http import request, route
from odoo.addons.sale.controllers.product_configurator import SaleProductConfiguratorController
from odoo.addons.website_sale.controllers.main import WebsiteSale



class NfWebsiteSaleProductConfiguratorController(SaleProductConfiguratorController, WebsiteSale):

    def _get_product_information(
        self,
        product_template,
        combination,
        currency,
        pricelist,
        so_date,
        quantity=1,
        product_uom_id=None,
        parent_combination=None,
        **kwargs,
    ):

        result = super()._get_product_information(product_template, combination, currency, pricelist, so_date, quantity, product_uom_id, parent_combination, **kwargs)
        result['nf_box_item_count'] = product_template.nf_box_item_count
        return result  