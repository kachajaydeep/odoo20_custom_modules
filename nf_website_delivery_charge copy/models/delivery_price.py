# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, _, http
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request

class nfWebsiteSaleDelivery(WebsiteSale):
    _express_checkout_delivery_route = '/shop/express/shipping_address_change'

    @http.route('/shop/nf_update_country', type='jsonrpc', auth='public', methods=['POST'], website=True, sitemap=False)
    def nf_update_country(self, country_id):
        cities = request.env['nf.cities'].search([('country_id', '=', int(country_id))])
        return cities.read()

    def _get_mandatory_address_fields(self, country_id=False):
        res = super()._get_mandatory_address_fields(country_id)
        res.remove('city')
        res.add('nf_city_id')
        return res
    
    def _prepare_address_form_values(self, *args, **kwargs):
        render_values = super()._prepare_address_form_values(*args, **kwargs)
        selected_country_id  = render_values['partner_sudo'].country_id.id
        order = render_values['website_sale_order']
        nf_city_id  = render_values['partner_sudo'].nf_city_id
        cities = request.env['nf.cities'].search([('country_id', '=', selected_country_id)])
        if cities:
            render_values['nf_cities'] = cities or []
            render_values['nf_city_id'] = nf_city_id
        else:
            render_values['nf_cities'] = []
            render_values['nf_city_id'] = False

        return render_values
    
    def _parse_form_data(self, form_data):
        """ Parse the form data and return them converted into address values and extra form data.

        :param dict form_data: The form data to convert to address values.
        :return: A tuple of converted address values and extra form data.
        :rtype: tuple[dict, dict]
        """
        address_values = {}
        extra_form_data = {}

        ResPartner = request.env['res.partner']
        partner_fields = ResPartner._fields
        authorized_partner_fields = set(
            request.env['ir.model']._get('res.partner')._get_form_writable_fields().keys()
        )
        authorized_partner_fields.add('nf_city_id')
        for key, value in form_data.items():
            if isinstance(value, str):
                value = value.strip()
            if key in partner_fields and key in authorized_partner_fields:
                if key ==  'nf_city_id':
                    city_id = request.env['nf.cities'].browse(int(form_data[key]))
                    address_values['city'] = city_id.name
                field = partner_fields[key]
                if field.type == 'many2one' and isinstance(value, str) and value.isdigit():
                    address_values[key] = field.convert_to_cache(int(value), ResPartner)
                else:
                    # Always keep field values, even if falsy, as it might be for resetting a field.
                    address_values[key] = field.convert_to_cache(value, ResPartner)
            elif value:  # The value cannot be saved on the `res.partner` model.
                extra_form_data[key] = value

        if (
            hasattr(ResPartner, 'check_vat')  # The `base_vat` module is installed.
            and address_values.get('vat')
            and address_values.get('country_id')
        ):
            address_values['vat'] = ResPartner.fix_eu_vat_number(
                address_values['country_id'],
                address_values['vat'],
            )

        return address_values, extra_form_data

class DeliveryPrice(models.Model):
    _inherit="delivery.price.rule"

    variable = fields.Selection( selection_add=[('city', 'City'),], ondelete={'city': 'cascade'},)
    nf_city_id = fields.Many2one('nf.cities', string="City")


class Deliverycarrier(models.Model):
    _inherit="delivery.carrier"

    def _get_price_from_picking(self, total, weight, volume, quantity, wv=0.):
        price = 0.0
        criteria_found = False
        order = request.cart
        price_dict = self._get_price_dict(total, weight, volume, quantity)
        for line in self.price_rule_ids:
            if line.variable == 'city':
                if order.partner_invoice_id.nf_city_id.id ==  line.nf_city_id.id:
                    price = line.list_base_price + line.list_price * price_dict[line.variable_factor]
                    criteria_found = True
                    break
            else:
                test = safe_eval(line.variable + line.operator + str(line.max_value), price_dict)
                if test:
                    price = line.list_base_price + line.list_price * price_dict[line.variable_factor]
                    criteria_found = True
                    break
        if not criteria_found:
            raise UserError(_("Not available for current order"))

        return price