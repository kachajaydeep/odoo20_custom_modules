# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import http, fields
from odoo.http import request
from odoo.tools.misc import format_amount
import json

class NfPriceCheckerController(http.Controller):
    def _format_price(self, amount, currency):
        """Helper to format price with currency symbol dynamically."""
        if not currency:
            return "{:,.2f}".format(amount)
        
        return format_amount(request.env, amount, currency)

    @http.route('/price_checker_kiosk', type='http', auth='public',website=True)
    def price_checker_kiosk(self, **kwargs):
        return request.render('nf_price_checker_kiosk.nf_price_checker_kiosk_template', {})
    
    @http.route('/price_checker_kiosk/get_product_data', type='jsonrpc', auth='public')
    def get_product_data(self, barcode):
        Product = request.env['product.product'].sudo()
        product = Product.search(['|', ('barcode', '=', barcode), ('default_code', '=', barcode)], limit=1)
        
        if not product:
            return {'error': 'Product not found'}
        
        company = request.env.company.sudo()
        ICPsudo = request.env['ir.config_parameter'].sudo()

        # ── Pricelist price ────────────────────────────────────────
        pricelist_prices = []
        show_pricelist = ICPsudo.get_bool('nf_price_checker_kiosk.nf_show_pricelist') == True
        param = ICPsudo.get_str('nf_price_checker_kiosk.nf_pricelist_ids', '[]')
        pricelist_ids = [int(i) for i in param.split(',') if i.strip().isdigit()]
        


        if show_pricelist and pricelist_ids:
            records = request.env['product.pricelist'].sudo().browse(pricelist_ids)

            for pl in records:
                if not pl.exists():
                    continue

                computed_price, rule_id = pl._get_product_price_rule(product, quantity=1.0)

                if not rule_id:
                    continue

                rule = request.env['product.pricelist.item'].sudo().browse(rule_id)
                compute_price = rule.compute_price if rule else 'fixed'

                discount_amount = 0.0
                if compute_price in ('percentage', 'formula') and product.lst_price:
                    discount_amount = max(computed_price, 0.0)

                pricelist_prices.append({
                    'name':            pl.name,
                    # 'price':           "{:,.2f}".format(computed_price),
                    # 'lst_price':       "{:,.2f}".format(product.lst_price),
                    'price':           self._format_price(computed_price, pl.currency_id),
                    'lst_price':       self._format_price(product.lst_price, company.currency_id),
                    'compute_price':   compute_price,
                    # 'discount_amount': "{:,.2f}".format(discount_amount),
                    'discount_amount': self._format_price(discount_amount, pl.currency_id),
                    'is_discounted':   compute_price in ('percentage', 'formula'),
                    
                })
        show_taxes = []
        if product.taxes_id:
            for record in product.taxes_id:
                if not record:
                    continue
                show_taxes.append(record.tax_label)
        print("\n\n\n\n product",product.weight)
        return {
            'id': product.id,
            'name': product.name,
            'default_code': product.default_code or '',
            'barcode': product.barcode or '',
            # 'lst_price': "{:,.2f}".format(product.lst_price),
            'lst_price': self._format_price(product.lst_price, company.currency_id),
            'pricelist_prices':  pricelist_prices, 
            'qty_available': product.qty_available,
            'description_sale': product.description_sale or '',
            'category': product.categ_id.name or '',
            'image_url': f'/web/image/product.product/{product.id}/image_1024',
            'company_logo': f'/web/image/res.company/{company.id}/logo',
            'taxes':show_taxes,
            'weight':product.weight,
            'company_name':request.env.company.name,
            
        }
    
    @http.route('/price_checker_kiosk/get_settings',type="jsonrpc",auth="public")
    def nf_get_price_checker_settings(self):
        ICPsudo = request.env['ir.config_parameter'].sudo()
        
        param = ICPsudo.get_str('nf_price_checker_kiosk.nf_pricelist_ids', '[]')
        pricelist_ids = [int(i) for i in param.split(',') if i.strip().isdigit()]
     
        pricelists = []

        pricelist_name = ''
        
        if pricelist_ids:
            records = request.env['product.pricelist'].sudo().browse(pricelist_ids)
            pricelists = [
                {'id': pl.id, 'name': pl.name}
                for pl in records if pl.exists()
            ]

        return {
            'nf_show_name': ICPsudo.get_bool('nf_price_checker_kiosk.nf_show_name'),
            'nf_show_image':ICPsudo.get_bool('nf_price_checker_kiosk.nf_show_image'),
            'nf_show_code':ICPsudo.get_bool('nf_price_checker_kiosk.nf_show_code'),
            'nf_show_barcode':ICPsudo.get_bool('nf_price_checker_kiosk.nf_show_barcode'),
            'nf_show_price':ICPsudo.get_bool('nf_price_checker_kiosk.nf_show_price'),
            'nf_show_stock':ICPsudo.get_bool('nf_price_checker_kiosk.nf_show_stock'),
            'nf_show_specification':ICPsudo.get_bool('nf_price_checker_kiosk.nf_show_specification'),
            'nf_show_category':ICPsudo.get_bool('nf_price_checker_kiosk.nf_show_category'),
            'nf_show_product_weight':ICPsudo.get_bool('nf_price_checker_kiosk.nf_show_product_weight'),
            'nf_show_product_sales_description':ICPsudo.get_bool('nf_price_checker_kiosk.nf_show_product_sales_description'),
            'nf_show_product_tax':ICPsudo.get_bool('nf_price_checker_kiosk.nf_show_product_tax'),
            'nf_show_keyboard':ICPsudo.get_bool('nf_price_checker_kiosk.nf_show_keyboard'),
            'nf_show_pricelist':ICPsudo.get_bool('nf_price_checker_kiosk.nf_show_pricelist'),
            'pricelists': pricelists,
            'nf_pricelist_name': pricelist_name,
            'company_logo': f'/web/image/res.company/{request.env.company.id}/logo',
            'company_name': request.env.company.name,
            'company_config_logo': ICPsudo.get_bool('nf_price_checker_kiosk.nf_company_logo'),
            'company_config_name': ICPsudo.get_bool('nf_price_checker_kiosk.nf_company_name'),
        }