from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TripPricelist(models.Model):
    _name = "trip.pricelist"
    _description = "Trip Pricelist"
    _rec_name = 'partner_id'
    _order = 'id'

    partner_id = fields.Many2one('res.partner', string='Shipper', domain=[('parent_id', '=', False)], required=True)
    amount = fields.Float('Shipper Price', required=True, tracking=True)
    target_amount = fields.Float('Target Price', required=True, tracking=True)
    product_id = fields.Many2one('product.product', string="Trip Product", required=True)
    fleet_type = fields.Selection([
        ('highsidea_truck', 'High Sides Truck'),
        ('lowbed_truck', 'Lowbed Truck'),
        ('flatbed_truck', 'Flatbed Truck'),
        ('lowsides_truck', 'Low Sides Truck'),
        ('curtain_truck', 'Curtain Truck'),
        ('lorry', 'Lorry'),
        ('dyna', 'Dyna'),
        ('jwanib', 'Jwanib'),
        ('tipper_truck', 'Tipper Truck'),
    ], string='Truck Type', default='flatbed_truck')

    @api.model
    def create(self, vals_list):
        res = super(TripPricelist, self).create(vals_list)
        for pricelist in res:
            body = """
            The Pricelist created for the Trip has been created!
            <ul>
                <li>Shipper <i class="fa fa-long-arrow-right"></i> %s</li>
                <li>Shipper Price <i class="fa fa-long-arrow-right"></i> %s</li>
                <li>Target Price <i class="fa fa-long-arrow-right"></i> %s</li>
            </ul>
            """ % (pricelist.partner_id.display_name, pricelist.amount, pricelist.target_amount)
            pricelist.product_id.message_post(body=body)
        return res

    def write(self, vals_list):
        body = """The Pricelist for the trip has been updated!"""
        if not vals_list.get('partner_id'):
            body = """The Pricelist for Shipper %s has been updated!""" % self.partner_id.display_name
        body += """<ul>"""
        for key, val in vals_list.items():
            if not vals_list.get('product_id'):
                field_detail = self.fields_get()[key]

                if field_detail['type'] == 'many2one':
                    old_value = self.read()[0][key][1]
                    new_value = self.env[field_detail['relation']].browse(val).display_name
                else:
                    old_value = self.read()[0][key]
                    new_value = val

                body += """<li>%s: %s <i class="fa fa-long-arrow-right"></i> %s</li>""" \
                        % (field_detail['string'], old_value, new_value)
        body += """</ul>"""

        res = super(TripPricelist, self).write(vals_list)
        self.product_id.message_post(body=body)
        return res


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    name = fields.Char('Name', index=True, required=True, translate=True, tracking=True)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    loading_point = fields.Many2one('trip.city', 'Loading Point', tracking=True)
    unloading_point = fields.Many2one('trip.city', 'Unloading Point', tracking=True)
    trip_pricelist_ids = fields.One2many('trip.pricelist', 'product_id', string='Trip Pricelists')
    shipper_ids = fields.Many2many('res.partner', compute='_compute_shipper', store=True)
    trip_ids = fields.One2many('itruck.trip', 'product_id', string="Trips", readonly=True,
                               domain=[('state', 'not in', ['in_review', 'draft', 'cancel', 'missed'])])

    # is_trip = fields.Boolean('Is Trip?', compute='_compute_is_product', store=True)
    #
    # @api.depends('loading_point', 'unloading_point')
    # def _compute_is_product(self):
    #     for product in self:
    #         product.is_trip = False
    #         if product.loading_point and product.unloading_point:
    #             product.is_trip = True

    @api.depends('trip_pricelist_ids.partner_id')
    def _compute_shipper(self):
        for product in self:
            shipper_ids = []
            for trip_pricelist in product.trip_pricelist_ids:
                shipper_ids.append(trip_pricelist.partner_id.id)
            product.shipper_ids = shipper_ids or False

    @api.onchange('loading_point', 'unloading_point')
    def onchange_points(self):
        if self.loading_point and self.unloading_point:
            self.name = f"Goods Trans from {self.loading_point.name} To {self.unloading_point.name}"

    @api.constrains('name', 'loading_point', 'unloading_point')
    def _constrain_duplicate_trip_name(self):
        for product in self:
            duplicate_trip_products = self.search([('id', '!=', product.id), ('loading_point', '!=', False)])
            for dup_product in duplicate_trip_products:
                if product.name.lower() == dup_product.name.lower():
                    raise ValidationError(_('Trip Product is already exist!!!'))
