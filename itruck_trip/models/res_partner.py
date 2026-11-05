from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
# from odoo.osv import expression
from lxml import etree


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    document_id = fields.Binary('Attachment')
    iban = fields.Char('IBAN', help="The IBAN of bank account")


class PartnerLicense(models.Model):
    _name = 'partner.license'
    _description = "Partner Licenses"

    name = fields.Char("License ID No.", required=True)
    partner_id = fields.Many2one('res.partner', "Partner")

    @api.constrains('name')
    def _constrains_driver_lic_id(self):
        for license in self:
            if license.name and len(license.name) != 10:
                raise ValidationError(_("ID Must be 10 characters!"))
            elif self.search([('name', '=', license.name), ('id', '!=', license.id)], limit=1):
                raise ValidationError(_("License ID must be unique!"))


class ResPartner(models.Model):
    _inherit = 'res.partner'

    team_id = fields.Many2one('crm.team', string='Sales Team', ondelete="set null")
    user_type = fields.Selection([('carrier', 'Carrier'), ('shipper', 'Shipper')], string="User Type")
    license_ids = fields.One2many('partner.license', 'partner_id', string='Driver Licenses')
    driver_lic_id = fields.Char('Driver ID')
    blacklisted = fields.Boolean('Blacklisted?', tracking=True)
    carrier_shipper_code = fields.Char('Carrier/Shipper Code', readonly=True)
    trip_count = fields.Integer('Trip Count', compute='_compute_trip_count')
    trip_pricelist_count = fields.Integer('Trip Pricelist Count', compute='_compute_trip_pricelist_count')
    trip_pricelist_ids = fields.One2many('trip.pricelist', 'partner_id', string='Trip Pricelists')
    company_registry = fields.Char('Company Registry')
    driver_dob = fields.Date(string='Driver DOB')
    license_expiry_date = fields.Date("License Expiry")
    parent_company = fields.Many2one('res.partner', 'Parent Company', domain=[('is_company', '=', True)])
    check_unpaid_trips = fields.Boolean('Check Unpaid Trips?', tracking=True,
                                        help="Check the past unpaid Trips and restrict to create new trips "
                                             "'Only for Shippers'")

    def _compute_trip_pricelist_count(self):
        for partner in self:
            partner.trip_pricelist_count = self.env['trip.pricelist'].search_count([('partner_id', '=', partner.id)])

    def _compute_trip_count(self):
        itruck = self.env['itruck.trip']
        for partner in self:
            trip_count = itruck.search_count([('partner_id', '=', partner.id)])
            if partner.user_type == 'carrier':
                trip_count = itruck.search_count([('vendor_id', '=', partner.id)])
            partner.trip_count = trip_count

    def action_view_trips(self):
        # view = self.env.ref('mail.email_compose_message_wizard_form')
        domain = [('partner_id', '=', self.id)]
        context = {'default_partner_id': self.id}
        if self.user_type == 'carrier':
            domain = [('vendor_id', '=', self.id)]
            context = {'default_vendor_id': self.id}
        return {
            'res_model': 'itruck.trip',
            'type': 'ir.actions.act_window',
            'name': _("Trips"),
            'domain': domain,
            'context': context,
            'view_mode': 'list,form',
            # 'view_id': view.id,
        }

    def action_view_trip_pricelist(self):
        # view = self.env.ref('mail.email_compose_message_wizard_form')
        return {
            'res_model': 'trip.pricelist',
            'type': 'ir.actions.act_window',
            'name': _("Trip Pricelist"),
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
            'view_mode': 'list',
            # 'view_id': view.id,
        }

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     if name:
    #         if self.env.context.get('search_by_shipper'):
    #             domain = ['|', ('carrier_shipper_code', 'ilike', name), ('name', 'ilike', name)]
    #             return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
    #         if self.env.context.get('search_by_lic'):
    #             domain = ['|', ('driver_lic_id', 'ilike', name), ('name', 'ilike', name)]
    #             return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
    #     return super()._name_search(name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        domain = args or []

        if name:
            if self.env.context.get('search_by_shipper'):
                domain = [
                    '|',
                    ('carrier_shipper_code', 'ilike', name),
                    ('name', 'ilike', name),
                    '&',
                    ('parent_id', '=', False),
                    ('user_type', '=', 'shipper'),
                ]
                partners = self.search_fetch(
                    domain, ['display_name'], limit=limit,
                )
                return [(partner.id, partner.display_name) for partner in partners]
            if self.env.context.get('search_by_lic'):
                domain = ['|', ('license_ids.name', 'ilike', name), ('name', 'ilike', name)]
                # domain = ['|', ('driver_lic_id', 'ilike', name), ('name', 'ilike', name)]
                partners = self.search_fetch(
                    domain, ['display_name'], limit=limit,
                )
                return [(partner.id, partner.display_name) for partner in partners]
        return super().name_search(name, domain, operator, limit)

    # def _get_name(self):
    #     name = super(ResPartner, self)._get_name()
    #     if self._context.get('display_street'):
    #         name = self.street or self.street2 or name
    #     return name

    @api.depends_context('display_street')
    def _compute_display_name(self):
        super()._compute_display_name()
        if self.env.context.get('display_street'):
            for partner in self:
                display_name = partner.street or partner.street2
                if display_name:
                    partner.display_name = display_name

    @api.model
    def create(self, values):
        if values.get('user_type'):
            if values['user_type'] == 'carrier':
                values['carrier_shipper_code'] = self.env['ir.sequence'].next_by_code('res.partner.carrier')
            else:
                values['carrier_shipper_code'] = self.env['ir.sequence'].next_by_code('res.partner.shipper')
        return super(ResPartner, self).create(values)

    def write(self, vals):
        if vals.get('user_type'):
            if vals['user_type'] == 'carrier':
                vals['carrier_shipper_code'] = self.env['ir.sequence'].next_by_code('res.partner.carrier')
            else:
                vals['carrier_shipper_code'] = self.env['ir.sequence'].next_by_code('res.partner.shipper')
        else:
            if 'user_type' in vals:
                vals['carrier_shipper_code'] = False
        res = super(ResPartner, self).write(vals)
        if vals.get('blacklisted'):
            if self.blacklisted:
                for partner in self.child_ids:
                    partner.blacklisted = True
                vehicles = self.env['fleet.vehicle'].search([('driver_id', '=', self.id), ('blacklisted', '=', False)])
                for vehicle in vehicles:
                    vehicle.blacklisted = True
        elif vals.get('blacklisted') == False:
            for partner in self.child_ids:
                if partner.blacklisted:
                    partner.blacklisted = False
            vehicles = self.env['fleet.vehicle'].search([('driver_id', '=', self.id), ('blacklisted', '=', True)])
            for vehicle in vehicles:
                vehicle.blacklisted = False
        return res

    def action_archive(self):
        res = super().action_archive()
        if self.carrier_shipper_code:
            self.carrier_shipper_code = False
        return res

    def action_unarchive(self):
        res = super().action_unarchive()
        if self.user_type:
            if self.user_type == 'carrier':
                code = self.env['ir.sequence'].next_by_code('res.partner.carrier')
            else:
                code = self.env['ir.sequence'].next_by_code('res.partner.shipper')
            self.carrier_shipper_code = code
        return res

    # @api.constrains('driver_lic_id')
    # def _constrains_driver_lic_id(self):
    #     for partner in self:
    #         if partner.driver_lic_id:
    #             if len(partner.driver_lic_id) != 10:
    #                 raise ValidationError(_("ID Must be 10 characters!"))
    #             if self.search([('id', '!=', partner.id), ('driver_lic_id', '=', partner.driver_lic_id)]):
    #                 raise ValidationError(_('The ID must be unique!'))

    @api.constrains('company_registry')
    def _constrains_company_registry(self):
        for partner in self:
            if partner.company_registry and len(partner.company_registry) > 10:
                raise ValidationError(_("You can't add more than 10 characters in CR(Company Registry)!"))

    @api.constrains('phone')
    def _constrains_custom_phone(self):
        for partner in self:
            if partner.phone and len(partner.phone) > 10:
                raise ValidationError(_("You can't add more than 10 characters in Phone!"))

    @api.constrains('mobile')
    def _constrains_custom_mobile(self):
        for partner in self:
            if partner.mobile and len(partner.mobile) > 10:
                raise ValidationError(_("You can't add more than 10 characters in Mobile!"))

    @api.constrains('vat')
    def _constrains_custom_vat(self):
        for partner in self:
            if partner.vat and len(partner.vat) > 15:
                raise ValidationError(_("You can't add more than 15 characters in Tax ID!"))

    @api.model
    def get_views(self, views, options=None):
        res = super().get_views(views, options)
        for view_type, view_info in res.get('views', {}).items():
            doc = etree.XML(view_info['arch'])
            if view_type in ['form']:
                for archform in doc.xpath("//form"):
                    archform.set('delete', '0')

                if not self.env.user.has_group('itruck_trip.group_contact_access_salesteam'):
                    for archform in doc.xpath("//group[@name='sale']/field[@name='user_id']"):
                        archform.set('readonly', '1')
                    for archform in doc.xpath("//group[@name='sale']/field[@name='team_id']"):
                        archform.set('readonly', '1')
                    for archform in doc.xpath("//field[@name='user_type']"):
                        archform.set('readonly', '1')
                if not self.env.user.has_group('itruck_trip.group_can_edit_contact'):
                    READONLY_FIELDS = ['parent_company', 'company_type', 'name', 'parent_id', 'branch_id', 'user_type',
                                       'carrier_shipper_code', 'street', 'street2', 'zip', 'city', 'state_id',
                                       'country_id', 'function', 'title', 'email', 'phone', 'mobile',
                                       'company_registry', 'vat', 'website', 'lang', 'category_id',
                                       'driver_lic_id', 'license_ids', 'driver_dob', 'blacklisted', 'blacklisted', 'image_1920',
                                       'l10n_sa_edi_plot_identification', 'l10n_sa_edi_building_number']
                    for node in doc.xpath("//field"):
                        if node.get('name') in READONLY_FIELDS:
                            node.set('readonly', '1')
            if view_type in ['list']:
                for archlist in doc.xpath("//list"):
                    archlist.set('delete', '0')
            view_info['arch'] = etree.tostring(doc, encoding='unicode')
        return res
