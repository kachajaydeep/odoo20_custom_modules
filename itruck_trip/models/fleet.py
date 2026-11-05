from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from lxml import etree


class FleetVehicleModel(models.Model):
    _inherit = 'fleet.vehicle.model'

    name = fields.Char(string='Model name', required=True, translate=True)


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    model_id = fields.Many2one('fleet.vehicle.model', 'Model', tracking=True, required=False,
                               help='Model of the vehicle',
                               default=lambda self: self.env['fleet.vehicle.model'].search([('brand_id', '=', self.env.ref('fleet.brand_mercedes').id)], limit=1))
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

    owner_id = fields.Many2one('res.partner', string='Owner', domain=[('is_company', '=', True)])
    owner_license_id = fields.Many2one('partner.license', string='Owner License', tracking=True,
                                       domain="[('partner_id', '=', owner_id)]")
    owner_lic_id = fields.Char(string='Owner ID', required=True)

    driver_license_id = fields.Many2one('partner.license', string='Driver License', tracking=True,
                                        domain="[('partner_id', '=', driver_id)]")
    driver_lic_id = fields.Char(related='driver_license_id.name', string='Driver ID')
    # driver_lic_id = fields.Char(related='driver_id.driver_lic_id', string='Driver ID')
    driver_phone = fields.Char(related='driver_id.phone', string='Phone')
    driver_dob = fields.Date(related='driver_id.driver_dob', string='Driver DOB')
    driver_lic_expiry_date = fields.Date(related='driver_id.license_expiry_date', string='Driver License Expiry')

    sequence_number = fields.Char(string="Sequence Number", required=True)

    blacklisted = fields.Boolean('Blacklisted?', tracking=True)
    trip_ids = fields.One2many('itruck.trip', 'fleet_id', string='Trips', readonly=True)

    monthly_rent = fields.Boolean('Monthly Rent?', tracking=True)

    operating_card_expiry = fields.Date("Operating Card Expiry")

    # @api.depends('model_id.brand_id.name', 'model_id.name', 'license_plate')
    # def _compute_vehicle_name(self):
    #     for record in self:
    #         record.name = record.license_plate or _('No Plate')

    @api.depends("license_plate")
    def _compute_display_name(self):
        super()._compute_display_name()
        for fleet in self:
            fleet.display_name = fleet.license_plate if fleet.license_plate else _('No Plate')

    @api.onchange('owner_id')
    def onchange_owner_id(self):
        if self.owner_id and self.owner_id.license_ids:
            self.owner_license_id = self.owner_id.license_ids[0].id
        # if self.owner_id and self.owner_id.driver_lic_id:
        #     self.owner_lic_id = self.owner_id.license_ids[0].name

    @api.onchange('driver_id')
    def onchange_driver_blacklisted(self):
        if self.driver_id and self.driver_id.license_ids:
            self.driver_license_id = self.driver_id.license_ids[0].id
        if self.driver_id and self.driver_id.blacklisted:
            self.blacklisted = True
            raise ValidationError(_("The Driver %s is Blacklisted!" % self.driver_id.name))
        else:
            self.blacklisted = False

    @api.onchange('owner_license_id')
    def onchange_owner_license_id(self):
        if self.owner_license_id:
            self.owner_lic_id = self.owner_license_id.name

    # @api.onchange('driver_license_id')
    # def onchange_driver_license_id(self):
    #     if self.driver_license_id:
    #         self.driver_lic_id = self.owner_license_id.name

    @api.model
    def get_views(self, views, options=None):
        res = super().get_views(views, options)
        for view_type, view_info in res.get('views', {}).items():
            doc = etree.XML(view_info['arch'])
            if view_type in ['form']:
                for archform in doc.xpath("//form"):
                    archform.set('delete', '0')

            if view_type in ['list']:
                for archlist in doc.xpath("//list"):
                    archlist.set('delete', '0')
            view_info['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    @api.constrains('sequence_number')
    def _constrains_sequence_number(self):
        for fleet in self:
            if fleet.sequence_number:
                if len(fleet.sequence_number) > 9:
                    raise ValidationError(_("You can't add more than 09 characters in Sequence Number!"))
                elif self.search([('sequence_number', '=', fleet.sequence_number), ('id', '!=', fleet.id)], limit=1):
                    raise ValidationError(_("Sequence Number must be unique!"))

    @api.constrains('owner_lic_id')
    def _constrains_owner_lic_id(self):
        for fleet in self:
            if fleet.owner_lic_id:
                if len(fleet.owner_lic_id) != 10:
                    raise ValidationError(_("Owner ID Must be 10 characters!"))
                # elif self.search([('name', '=', license.name), ('id', '!=', license.id)], limit=1):
                #     raise ValidationError(_("License ID must be unique!"))
