# import qrcode
# import base64
# from io import BytesIO
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, AccessError
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from lxml import etree


class TripProductType(models.Model):
    _name = "trip.product.type"
    _description = "Trip Product Type"
    _rec_name = "name"

    name = fields.Char('Product Type', required=True, translate=True)


class ItruckTrip(models.Model):
    _name = 'itruck.trip'
    _description = "Trip"
    _inherit = ['mail.thread']
    _rec_name = "name"
    _order = 'id desc'

    name = fields.Char('Trip Number', required=True, copy=False, readonly=True, default=lambda x: _('New'))
    product_id = fields.Many2one('product.product', 'Trip Details', domain=[('loading_point', '!=', False)], required=True,
                                 tracking=True)
    date = fields.Date('Trip Date', required=True, tracking=True)
    arrival_date = fields.Date('Arrival Date', tracking=True)
    loading_point = fields.Many2one(related='product_id.loading_point', string='Loading Point', store=True,
                                    tracking=True)
    unloading_point = fields.Many2one(related='product_id.unloading_point', string='Unloading Point', store=True,
                                      tracking=True)
    product_type_id = fields.Many2one('trip.product.type', string='Product Type', required=True, tracking=True)
    weight = fields.Float('Weight', required=True)
    uom_id = fields.Many2one('uom.uom', 'Unit of Measure')
    amount = fields.Float('Shipper Price', required=True, tracking=True)
    user_id = fields.Many2one('res.users', 'Salesperson', required=True, tracking=True)
    team_id = fields.Many2one('crm.team', string='Sales Team', check_company=True, index=True, tracking=True,
                              domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                              compute='_compute_team_id', ondelete="set null", readonly=False, store=True)
    partner_id = fields.Many2one('res.partner', 'Shipper', required=True, tracking=True,
                                 domain=['&', ('parent_id', '=', False), ('user_type', '=', 'shipper')])
    partner_shipping_id = fields.Many2one('res.partner', string='Pickup Address',
                                          domain="[('parent_id', '=', partner_id), ('type', '=', 'delivery')]")
    shipping_comment = fields.Html(related='partner_shipping_id.comment', string='Pickup Notes')
    dropoff_address_id = fields.Many2one('res.partner', string='Drop-off Address',
                                         domain="[('parent_id', '=', partner_id), ('type', '=', 'delivery')]")
    dropoff_comment = fields.Html(related='dropoff_address_id.comment', string='Drop-off Notes')
    shipper_fleet_type = fields.Selection([
        ('flatbed_truck', 'Flatbed Truck'),
        ('highsidea_truck', 'High Sides Truck'),
        ('lowbed_truck', 'Lowbed Truck'),
        ('lowsides_truck', 'Low Sides Truck'),
        ('curtain_truck', 'Curtain Truck'),
        ('lorry', 'Lorry'),
        ('dyna', 'Dyna'),
        ('jwanib', 'Jwanib'),
        ('tipper_truck', 'Tipper Truck'),
    ], string='Truck Type', default='flatbed_truck')
    consignee_id = fields.Many2one('res.partner', 'Consignee', domain="[('parent_id', '=', partner_id)]", tracking=True)
    consignee_phone = fields.Char(string='Consignee Phone')
    delivery_note = fields.Binary('Delivery Note')
    transport_document = fields.Binary('Transport Document')
    state = fields.Selection([
        ('in_review', 'In Review'),
        ('draft', 'Pending'),
        ('confirm', 'Booked'),
        ('in_process', 'Ongoing'),
        ('completed', 'Delivered'),
        ('in_invoice', 'Ready to Invoice'),
        ('invoiced', 'Invoiced'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ('missed', 'Missed')], string='Status', default='draft', tracking=True)
    note = fields.Text('Note')
    # Carrier
    carrier_type = fields.Selection([
        ('company', 'Company'),
        ('individual', 'Freelancer')], string='Carrier Payment Type', tracking=True)
    carrier_type2 = fields.Selection([
        ('company', 'Company'),
        ('individual', 'Freelancer')], string='Carrier Type', tracking=True)
    vendor_id = fields.Many2one('res.partner', 'Carrier', tracking=True)
    vendor_user_id = fields.Many2one(related='vendor_id.user_id', string='Carrier Salesperson', store=True)
    fleet_type = fields.Selection(related='fleet_id.fleet_type', string='Truck Type', tracking=True)
    license_plate = fields.Char(related='fleet_id.license_plate', string='License Plate')
    owner_id = fields.Many2one(related='fleet_id.owner_id', string='Owner Name', tracking=True, store=True)
    owner_lic_id = fields.Char(related='fleet_id.owner_lic_id', string='Owner ID', tracking=True, store=True)
    carrier_amount = fields.Float('Carrier Price', tracking=True)

    driver_id = fields.Many2one('res.partner', string='Driver', tracking=True)
    fleet_id = fields.Many2one('fleet.vehicle', 'Plate No.',
                               domain="[('model_id', '!=', False), ('license_plate', '!=', False)]", tracking=True)
    driver_license_id = fields.Many2one('partner.license', string='Driver License', tracking=True,
                                        domain="[('partner_id', '=', driver_id)]")
    driver_lic_id = fields.Char(related='driver_license_id.name', string='Driver ID', tracking=True)
    # driver_lic_id = fields.Char(related='driver_id.driver_lic_id', string='Driver ID', tracking=True)
    driver_phone = fields.Char(related='fleet_id.driver_phone', string='Driver Phone', tracking=True)
    driver_dob = fields.Date(related='fleet_id.driver_dob', string='Driver DOB', tracking=True)
    sequence_number = fields.Char(related='fleet_id.sequence_number', string='Sequence Number', tracking=True)
    monthly_rent = fields.Boolean(related='fleet_id.monthly_rent', string='Monthly Fleet Rent?')
    dn_number = fields.Char('D/N No.')
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)
    target_amount = fields.Float('Target Price', tracking=True, compute='_compute_target_amount', store=True,
                                 readonly=False)
    readonly_target_amount = fields.Boolean()
    invoice_id = fields.Many2one('account.move', 'Invoice', tracking=True,
                                 domain="[('partner_id', '=', partner_id), "
                                        "('move_type', '=', 'out_invoice'), "
                                        "('state', '=', 'draft')]")
    invoice_payment_status = fields.Selection(related='invoice_id.payment_state', string='Collect Status', store=True)
    bill_id = fields.Many2one('account.move', 'Bill', tracking=True,
                              domain="[('partner_id', '=', vendor_id), "
                                     "('move_type', '=', 'in_invoice'), "
                                     "('state', '=', 'draft')]")
    individual_entry = fields.Many2one('account.move', 'Freelancer Entry', tracking=True)
    accrued_entry = fields.Many2one('account.move', 'Accrued Entry', tracking=True)

    journal_id = fields.Many2one('account.journal', string='Journal',
                                 domain="[('type', 'in', ['cash', 'bank', 'general'])]")
    account_id = fields.Many2one('account.account', string='Bank Account')

    receiver_id = fields.Many2one('res.users', string='Receiver', readonly=True, tracking=True)
    dor = fields.Date(string='DOR', help='Date of Receiving Delivery', readonly=True, tracking=True)
    received_status = fields.Selection([
        ('no', 'Not Received'),
        ('yes', 'Received'),
        ('late', 'Late'),
        ('missing', 'Missing'),
        ('na', 'N/A')
    ], string='Delivery Note Status', default='no', tracking=True)
    payment_status = fields.Selection([('unpaid', 'Unpaid'), ('paid', 'Paid')], string='Payment Status', tracking=True)
    # payment_status = fields.Selection([('paid', 'Fully Paid'), ('partial', 'Partially Paid'),
    #                                    ('unpaid', 'Unpaid')], string='Payment Status', tracking=True)
    payment_amount = fields.Float('Payment Amount', tracking=True)
    account_payment_status = fields.Selection(
        [
            ('unpaid', 'Unpaid'),
            ('in_payment', 'In Payment'),
            ('paid', 'Paid'),
            ('partial', 'Partially Paid'),
            ('reversed', 'Reversed'),
            ('invoicing_legacy', 'Invoicing App Legacy'),
        ], string='Account Payment Status', default='unpaid', tracking=True,
        compute='_compute_account_payment_status', store=True)

    employee_id = fields.Many2one('hr.employee', string="Covered By", tracking=True)
    active = fields.Boolean(default=True, string='Archive', tracking=True)
    payment_date = fields.Date('Payment Date', default=fields.Date.today)

    tag_ids = fields.Many2many('trip.tag', 'trip_tag_rel', 'trip_id', 'tag_id', string='Tags',
                               help="Classify and analyze your Trip categories like: Training, Service")
    bank_partner_id = fields.Many2one(comodel_name='res.partner', string="Bank Carrier/Driver",
                                      compute='_compute_bank_partner_id')
    partner_bank_ids = fields.Many2many(comodel_name='res.partner.bank', string="Bank Accounts")
    acc_holder_name = fields.Char(compute='_compute_partner_bank', string='Account Holder Name')
    bank_id = fields.Many2one('res.bank', compute='_compute_partner_bank', string='Bank')
    canceled_by = fields.Selection([
        ('by_shipper', 'Canceled by Shipper'),
        ('by_driver', 'Canceled by Driver')], string='Canceled By', tracking=True)
    collected_by_cash = fields.Boolean(string='Collected By Cash?', tracking=True)
    collection_date = fields.Date(string='Collection Date', tracking=True)
    received_by = fields.Many2one('res.users', string='Received By', tracking=True)

    profit = fields.Float('Profit', compute='_compute_profit_margin', store=True)
    margin = fields.Float('Margin(%)', compute='_compute_profit_margin', store=True)

    @api.depends('amount', 'carrier_amount')
    def _compute_profit_margin(self):
        for trip in self:
            trip.profit = trip.amount - trip.carrier_amount
            trip.margin = (trip.profit/trip.amount) * 100 if trip.profit and trip.amount else 0.0

    @api.depends('carrier_type', 'individual_entry', 'bill_id', 'bill_id.payment_state')
    def _compute_account_payment_status(self):
        for trip in self:
            account_payment_status = 'unpaid'
            if trip.carrier_type == 'individual' and trip.individual_entry:
                account_payment_status = 'paid'
            if trip.carrier_type == 'company' and trip.bill_id and trip.bill_id.payment_state != 'not_paid':
                account_payment_status = trip.bill_id.payment_state
            trip.account_payment_status = account_payment_status

    def _compute_bank_partner_id(self):
        for trip in self:
            bank_partner_id = False
            if trip.carrier_type == 'company':
                if trip.vendor_id:
                    bank_partner_id = trip.vendor_id.id
            else:
                if trip.driver_id:
                    bank_partner_id = trip.driver_id.id
            trip.bank_partner_id = bank_partner_id or False

    @api.onchange('carrier_type', 'vendor_id', 'driver_id')
    def onchange_partner_bank_ids(self):
        if self.vendor_id.blacklisted:
            raise ValidationError(_("The Carrier '%s' is Blacklisted!" % self.vendor_id.name))
        if self.carrier_type:
            partner_bank_ids = False
            if self.carrier_type == 'company':
                if self.vendor_id:
                    partner_bank_ids = self.vendor_id.bank_ids
                    for bank_id in partner_bank_ids:
                        bank_id.acc_holder_name = self.vendor_id.name
            else:
                if self.driver_id:
                    partner_bank_ids = self.driver_id.bank_ids
                    for bank_id in partner_bank_ids:
                        bank_id.acc_holder_name = self.driver_id.name
            self.partner_bank_ids = partner_bank_ids.ids if partner_bank_ids else False

    def _compute_partner_bank(self):
        for trip in self:
            acc_holder_name = False
            bank_id = False
            if trip.partner_bank_ids:
                acc_holder_name = trip.partner_bank_ids[0].acc_holder_name
                bank_id = trip.partner_bank_ids[0].bank_id
            trip.acc_holder_name = acc_holder_name
            trip.bank_id = bank_id.id if bank_id else False

    # qr_code = fields.Binary(string="QR Code", compute='generate_qr_code', attachment=True, store=True)
    #
    # @api.model
    # def generate_qr_code(self):
    #     qr = qrcode.QRCode(
    #         version=1,
    #         error_correction=qrcode.constants.ERROR_CORRECT_L,
    #         box_size=10,
    #         border=4,
    #     )
    #     data = f"Trip No. : {self.name}\n" \
    #            f"Date : {self.date}\n" \
    #            f"Loading Point : {self.loading_point}\n" \
    #            f"Unloading Point : {self.unloading_point}\n" \
    #            f"Commodity : {self.product_type_id.name}\n"
    #     qr.add_data(data)
    #     qr.make(fit=True)
    #     img = qr.make_image()
    #     temp = BytesIO()
    #     img.save(temp, format="PNG")
    #     qr_image = base64.b64encode(temp.getvalue())
    #     self.qr_code = qr_image

    @api.depends('product_id', 'partner_id', 'shipper_fleet_type')
    def _compute_target_amount(self):
        for trip in self:
            target_amount = 0.0
            if trip.product_id:
                for trip_pricelist in trip.product_id.trip_pricelist_ids:
                    if trip_pricelist.partner_id.id == trip.partner_id.id:
                        # target_amount = trip_pricelist.target_amount
                        if trip_pricelist.fleet_type == trip.shipper_fleet_type:
                            target_amount = trip_pricelist.target_amount
                            break
            trip.target_amount = target_amount
            if target_amount > 0.0:
                trip.readonly_target_amount = True
            else:
                trip.readonly_target_amount = False

    @api.depends('user_id')
    def _compute_team_id(self):
        """ When changing the user, also set a team_id or restrict team id
        to the ones user_id is member of. """
        for trip in self:
            # setting user as void should not trigger a new team computation
            if trip.partner_id.team_id:
                team = trip.partner_id.team_id
            else:
                if not trip.user_id:
                    continue
                user = trip.user_id
                if trip.team_id and user in (trip.team_id.member_ids | trip.team_id.user_id):
                    continue
                team = self.env['crm.team']._get_default_team_id(user_id=user.id)
            trip.team_id = team.id

    @api.model
    def create(self, vals):
        context = {'mail_create_nosubscribe': True, 'mail_auto_subscribe_no_notify': True}
        if not self.env.user.has_group('itruck_trip.group_contact_access_salesteam') and vals.get('partner_id'):
            partner = self.env['res.partner'].browse(vals['partner_id'])
            if partner.exists() and partner.check_unpaid_trips:
                check_date = fields.Date.today() - timedelta(days=60)
                trip = self.env[self._name].search([('partner_id', '=', vals['partner_id']),
                                                    ('invoice_id.payment_state', '=', 'not_paid'),
                                                    ('date', '<', check_date)], limit=1)
                if trip:
                    raise ValidationError(_("The shipper has outstanding trips unpaid for over 60 days. "
                                            "Please contact the administration for assistance."))
        res = super(ItruckTrip, self.with_context(context)).create(vals)

        seq_obj = self.env['ir.sequence']
        seq_id = seq_obj.search([('code', '=', self._name)], limit=1)
        if not seq_id.use_date_range:
            seq_id.use_date_range = True
            seq_id.range_reset = 'daily'
        city_code = '00'
        date = fields.datetime.today().strftime("%d%m%y")
        if vals.get('loading_point'):
            city_code = self.env['trip.city'].browse(vals['loading_point']).code
        res.name = '8' + city_code + date + str(seq_obj.next_by_code(self._name)) or _('New')

        # if vals.get('carrier_type'):
        #     if res.carrier_type == 'company':
        #         if res.accrued_entry:
        #             if res.accrued_entry.state == 'posted':
        #                 res.accrued_entry.button_draft()
        #             res.accrued_entry.unlink()
        #     elif res.carrier_type == 'individual':
        #         if not res.accrued_entry and res.carrier_amount:
        #             res.create_accrued_entry()
        return res

    def write(self, vals):
        old_tag_ids = {}
        if 'tag_ids' in vals and not self.env.user.has_group('itruck_trip.group_trip_manager'):
            for trip in self:
                old_tag_ids[trip.id] = trip.tag_ids.ids

        res = super(ItruckTrip, self).write(vals)

        if 'tag_ids' in vals and not self.env.user.has_group('itruck_trip.group_trip_manager'):
            for trip in self:
                for tag in old_tag_ids[trip.id]:
                    if tag not in trip.tag_ids.ids:
                        raise ValidationError(_("You don't have access to change the Tags of the Trip"))

        if vals.get('individual_entry') and self.id not in self.individual_entry.line_ids.trip_id.ids:
            individual_entry = self.individual_entry.with_context(pass_check_balanced=True)
            account_id = self.env.ref('account.1_sa_account_400013')
            # account_id = self.env['account.account'].sudo().search([('code', '=', '300008')], limit=1)
            if not account_id:
                raise ValidationError("400013 Transportation Expenses For Others account "
                # raise ValidationError("300008 Owner's Current Account (Freelancer) "
                                      "isn't find please create first!!!")
            individual_entry.write({'line_ids': [
                (0, 0, {'account_id': account_id.id, 'debit': self.carrier_amount,
                        'trip_id': self.id, 'name': f"[{self.name}] {self.product_id.name}"})]})
            credit_lines = individual_entry.line_ids.filtered(lambda l: l.credit > 0.0 or l.debit == 0.0)
            matched_credit_account_id = False
            for credit_line in credit_lines:
                if credit_line.account_id == self.account_id:
                    matched_credit_account_id = True
                    credit_line.write({'credit': credit_line.credit + self.carrier_amount})
            if not matched_credit_account_id:
                credit_lines[0].write({'credit': credit_lines[0].credit + self.carrier_amount})

        # if vals.get('carrier_type') and not vals.get('accrued_entry'):
        #     if self.carrier_type == 'company':
        #         if self.accrued_entry:
        #             if self.accrued_entry.state == 'posted':
        #                 self.accrued_entry.button_draft()
        #             self.accrued_entry.unlink()
        #     elif self.carrier_type == 'individual':
        #         if not self.accrued_entry and self.carrier_amount:
        #             self.create_accrued_entry()
        return res

    @api.onchange('received_status')
    def onchange_received_status(self):
        if self.received_status == 'late':
            raise ValidationError(_("You can't change Delivery Note Status to 'Late'!"))
        self.write({'receiver_id': self.env.user.id, 'dor': fields.Datetime.now().date()})

    @api.onchange('consignee_id')
    def onchange_consignee_id(self):
        consignee_phone = False
        if self.consignee_id:
            consignee_phone = self.consignee_id.phone
        self.consignee_phone = consignee_phone

    @api.onchange('product_id', 'partner_id', 'shipper_fleet_type')
    def onchange_product_id(self):
        amount = 0.0
        if self.product_id:
            for trip_pricelist in self.product_id.trip_pricelist_ids:
                if trip_pricelist.partner_id.id == self.partner_id.id:
                    # amount = trip_pricelist.amount
                    if trip_pricelist.fleet_type == self.shipper_fleet_type:
                        amount = trip_pricelist.amount
                        break
        self.amount = amount
        if self.partner_id:
            if self.partner_id.blacklisted:
                raise ValidationError(_("The Shipper '%s' is Blacklisted!" % self.partner_id.name))
            self.partner_shipping_id = self.partner_id.address_get(['delivery'])['delivery']
        else:
            self.partner_shipping_id = False
        if self.partner_id and self.partner_id.user_id:
            self.user_id = self.partner_id.user_id.id
        else:
            self.user_id = self.env.user.id

    @api.onchange('carrier_type')
    def domain_vendor_id(self):
        if self.carrier_type == 'company':
            return {'domain': {'vendor_id': [('is_company', '=', True)]}}
        elif self.carrier_type == 'individual':
            return {'domain': {'vendor_id': [('is_company', '=', False)]}}

    # @api.onchange('carrier_type')
    # def onchange_carrier_type(self):
    #     if self.carrier_type == 'company':
    #         if self.accrued_entry:
    #             if self.accrued_entry.state == 'posted':
    #                 self.accrued_entry.button_draft()
    #             self.accrued_entry.unlink()
    #     elif self.carrier_type == 'individual':
    #         if not self.accrued_entry and self.carrier_amount:
    #             self.create_accrued_entry()

    @api.constrains('received_status')
    def _check_received_status(self):
        for trip in self:
            error = ""
            if trip.received_status == 'yes':
                if not trip.dn_number:
                    error = "Please add the D/N No.!!!"
                if not trip.delivery_note:
                    error = "Please add the Delivery Note!!!"
                if not trip.payment_status:
                    error = "Please set the Payment Status!!!"
            if error:
                raise ValidationError(_(error))

    @api.constrains('state')
    def _check_state(self):
        for trip in self:
            error = ""
            if trip.state == 'in_invoice':
                if trip.received_status == 'yes':
                    if not trip.delivery_note:
                        error = "Please add the Delivery Note!!!"
                    if not trip.payment_status:
                        error = "Please set the Payment Status!!!"
                    elif trip.payment_status == 'paid' and trip.payment_amount <= 0.0:
                        error = "Please fill the Payment Amount!!!"

                if not trip.received_status:
                    error = "Please set the Received Status!!!"
            if error:
                raise ValidationError(_(error))

    @api.constrains('carrier_amount', 'target_amount')
    def _check_carrier_target_amount(self):
        for trip in self:
            if trip.target_amount and trip.carrier_amount > trip.target_amount and not self.env.user.has_group(
                    'itruck_trip.group_trip_manager'):
                raise AccessError(_("You haven't access to set Carrier Price higher than the Target Price, "
                                    "Please Contact your Administrator!!!"))

    # @api.onchange('payment_status')
    # def onchange_payment_status(self):
    #     if self.payment_status == 'partial':

    @api.onchange('delivery_note')
    def onchange_delivery_note(self):
        if not self.received_status:
            received_status = 'no'
            if self.delivery_note:
                received_status = 'yes'
            self.received_status = received_status
        if self.delivery_note:
            self.action_in_invoice()

    @api.onchange('dn_number')
    def onchange_dn_number(self):
        if self.dn_number and self.invoice_id:
            move_line = self.invoice_id.invoice_line_ids.filtered(lambda l: l.trip_id and l.trip_id.id == self._origin.id)
            if move_line:
                move_line.write({'dn_number': self.dn_number})

    @api.onchange('driver_id')
    def onchange_driver_id(self):
        if self.driver_id:
            if self.driver_id.license_ids:
                self.driver_license_id = self.driver_id.license_ids[0].id
            # self.fleet_id = self.env['fleet.vehicle'].search([('driver_id', '=', self.driver_id.id)], limit=1)

            if self.driver_id.blacklisted:
                raise ValidationError(_("The Driver %s is Blacklisted!" % self.driver_id.name))
        else:
            self.driver_license_id = False
            # self.fleet_id = False

    @api.onchange('fleet_id')
    def onchange_fleet_id(self):
        fleet_id = self.fleet_id
        if fleet_id:
            if fleet_id.driver_id:
                self.driver_id = fleet_id.driver_id.id
            if fleet_id.owner_id:
                if fleet_id.owner_id.parent_company:
                    self.vendor_id = fleet_id.owner_id.parent_company.id
                else:
                    self.vendor_id = fleet_id.owner_id.id
            if fleet_id.blacklisted:
                raise ValidationError(
                    _("The Plate No./Carrier %s is Blacklisted!" % fleet_id.license_plate or fleet_id.model_id.name))
            if fleet_id.tag_ids:
                tag_obj = self.env['trip.tag']
                tags = []
                for tag_id in fleet_id.tag_ids:
                    trip_tag = tag_obj.search([('name', 'ilike', tag_id.name)], limit=1)
                    if not trip_tag:
                        trip_tag = tag_obj.create({'name': tag_id.name})
                    tags.append(trip_tag.id)
                if tags:
                    if self.tag_ids:
                        tags += self.tag_ids.ids
                    self.tag_ids = tags

    def action_in_review(self):
        self.write({
            'state': 'in_review',
            # 'invoice_id': False
        })

    def action_draft(self):
        self.write({
            'state': 'draft',
            # 'invoice_id': False
        })

    def action_confirm(self):
        if self.vendor_id.blacklisted:
            raise ValidationError(_("The Carrier '%s' is Blacklisted!" % self.vendor_id.name))
        if self.driver_id.blacklisted:
            raise ValidationError(_("The Driver '%s' is Blacklisted!" % self.driver_id.name))
        fleet_id = self.fleet_id
        if fleet_id.blacklisted:
            raise ValidationError(
                _("The Plate No./Carrier '%s' is Blacklisted!" % fleet_id.license_plate or fleet_id.model_id.name))

        if not self.sequence_number:
            raise ValidationError(_("Sequence Number is mandatory on the Plate No.!!!"))
        elif self.carrier_amount <= 0.0:
            raise ValidationError(_("Can't update the Trip status because the Carrier Price empty!!!"))
        # elif not self.carrier_type:
        #     raise ValidationError(_("Please set the Carrier Payment Type!!!"))
        elif not self.carrier_type2:
            raise ValidationError(_("Please set the Carrier Type!!!"))
        elif not self.vendor_id:
            raise ValidationError(_("Please set the Carrier!!!"))
        elif not self.owner_lic_id:
            raise ValidationError(_("Please set the Owner ID!!!"))

        # if not self.env.user.has_group('itruck_trip.group_trip_manager') and self.employee_id and self.vendor_user_id:
        #     if self.employee_id.user_id != self.vendor_user_id:
        #         raise ValidationError(_("Carrier’s salesperson must matched with the covered by!!!"))

        if self.state == 'draft':
            self.state = 'confirm'

    def action_in_process(self):
        # Status change to Ongoing
        if self.state == 'confirm':
            self.state = 'in_process'

    def action_completed(self):
        # Status change to Delivered
        if self.state == 'in_process':
            self.state = 'completed'
            # if self.carrier_type == 'individual':
            #     self.action_done()
            # else:
            #     self.state = 'completed'

    def action_in_invoice(self):
        if not self.carrier_type:
            raise ValidationError(_("Please set the Carrier Payment Type!!!"))
        if self.state == 'completed':
            if not self.dn_number and self.received_status == 'yes':
                raise ValidationError(_("D/N No. isn't set!!!"))
            self.state = 'in_invoice'

    def action_done(self):
        # if self.state in ['in_invoice', 'in_process', 'completed']:
        if self.state in ['in_invoice', 'invoiced']:
            # if not self.account_payment_status:
            #     raise ValidationError(_("Account Payment status isn't set!!!"))
            if not self.payment_date:
                raise ValidationError(_("Payment Date isn't set!!!"))
            self.account_payment_status = 'paid'
            self.state = 'done'
            if self.carrier_type == 'individual' and not self.individual_entry:
                account_id = self.env.ref('account.1_sa_account_400013')
                # account_id = self.env['account.account'].sudo().search([('code', '=', '300008')], limit=1)
                if not account_id:
                    raise ValidationError("400013 Transportation Expenses For Others account "
                    # raise ValidationError("300008 Owner's Current Account (Freelancer) "
                                          "isn't find please create first!!!")
                if not self.journal_id:
                    raise ValidationError("Journal isn't set!!!")
                elif not self.account_id:
                    raise ValidationError("Account isn't set!!!")
                # elif not account_id:
                #     raise ValidationError("201021 Accrued Transportation Expenses For Others Account "
                #                           "isn't find please create first!!!")

                ref = f"[{self.name}] {self.product_id.name}"
                vals = {
                    'ref': ref,
                    'date': self.payment_date or fields.Date.today(),
                    'move_type': 'entry',
                    'journal_id': self.journal_id.id,
                    'line_ids': [
                        (0, 0, {'account_id': account_id.id, 'debit': self.carrier_amount, 'name': ref, 'trip_id': self.id}),
                        (0, 0, {'account_id': self.account_id.id, 'credit': self.carrier_amount, 'name': ref}),
                    ]
                }
                journal_entry = self.env['account.move'].create(vals)
                if journal_entry:
                    self.individual_entry = journal_entry.id

    def action_cancel(self):
        # if self.invoice_id:
        #     if self.invoice_id.payment_state in ['paid', 'partial']:
        #         raise ValidationError(_('The Payment is already has been created, \n '
        #                                 'if you want to cancel the trip, Cancel the Payment of the Invoice first!'))
        #     else:
        #         self.invoice_id.button_cancel()
        # if self.bill_id:
        #     if self.bill_id.payment_state in ['paid', 'partial']:
        #         raise ValidationError(_('The Payment is already has been created, \n '
        #                                 'if you want to cancel the trip, Cancel the Payment of the Bill first!'))
        #     else:
        #         self.bill_id.button_cancel()
        # self.write({'state': 'cancel'})
        return {
            'name': _('Cancel Trip'),
            'res_model': 'trip.cancel.by',
            'view_mode': 'form',
            'context': {'default_trip_ids': self.ids},
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    def action_trip_account_move(self):
        move_type = self._context.get('move_type')
        if len(self.partner_id.ids) > 1 and move_type == 'out_invoice':
            raise ValidationError(_("Please select only one shipper Trips!!!"))
        context = {
            'default_trip_ids': self.ids,
            'default_move_type': 'out_invoice',
            'default_partner_id': self.partner_id.id,
        }
        if self._context.get('create_from_form'):
            context.update({'create_from_form': True})
        if move_type == 'in_invoice':
            if len(self.vendor_id.ids) > 1:
                raise ValidationError(_("Please select only one carrier Trips!!!"))
            context.update({'default_move_type': move_type, 'default_partner_id': self.vendor_id.id})
        return {
            'name': _('Create Invoice/Bills'),
            'res_model': 'trip.account.move',
            'view_mode': 'form',
            'context': context,
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    # def create_accrued_entry(self):
    #     credit_account_id = self.env['account.account'].search([('code', '=', '201021')], limit=1)
    #     debit_account_id = self.env.ref('account.1_sa_account_400013')
    #     journal_id = self.env['account.journal'].search([('code', '=', 'MISC')], limit=1)
    #
    #     if credit_account_id and debit_account_id and journal_id:
    #         entry_name = f"{self.name} + {self.product_id.name}"
    #         journal_entry = self.env['account.move'].create({
    #             'ref': f"[{self.name}] + {self.product_id.name} + {self.partner_id.name}",
    #             'date': self.date or fields.Date.today(),
    #             'move_type': 'entry',
    #             'journal_id': journal_id.id,
    #             'line_ids': [
    #                 (0, 0, {'account_id': debit_account_id.id, 'debit': self.carrier_amount,
    #                         'trip_id': self.id, 'name': entry_name}),
    #                 (0, 0, {'account_id': credit_account_id.id, 'credit': self.carrier_amount, 'name': entry_name}),
    #             ]
    #         })
    #         if journal_entry:
    #             self.accrued_entry = journal_entry.id

    def _cron_create_accrued_entries_missed_trip(self):
        ## For Accrued Entry
        # trips = self.search([('accrued_entry', '=', False),
        #                      ('carrier_type', '=', 'individual'),
        #                      ('state', '=', 'confirm')])
        # for trip in trips:
        #     trip.create_accrued_entry()

        ## For Missed Trips
        missed_trips = self.search([('state', '=', 'draft'),
                                    ('create_date', '<', fields.datetime.now() - timedelta(days=2))])
        for missed_trip in missed_trips:
            missed_trip.state = 'missed'

    def _cron_check_trip_received_status(self):
        today = fields.Date.today()

        # ------------------------------------------------------------------
        # A) Mark as MISSING (60 days from date)
        # ------------------------------------------------------------------
        missing_trips_domain = [
            ('received_status', 'in', [False, 'no']),
            ('date', '<=', today - timedelta(days=60)),
            ('state', '=', 'completed'),
            ('delivery_note', '=', False),
        ]
        missing_trips = self.sudo().search(missing_trips_domain)
        missing_trips.write({'received_status': 'missing'})

        # ------------------------------------------------------------------
        # B) Mark LATE → Trips 1–25 (late after same month ends)
        # ------------------------------------------------------------------
        late_trips_domain = [('received_status', 'in', [False, 'no'])]

        late_trips = self.sudo().search(late_trips_domain)
        trips_1_25 = late_trips.filtered(lambda t: 1 <= t.date.day <= 25)


        for rec in trips_1_25:
            last_day_month = rec.date.replace(day=1) + relativedelta(months=1) - timedelta(days=1)
            if today >= last_day_month:
                rec.received_status = 'late'

        # ------------------------------------------------------------------
        # C) Mark LATE → Trips 26–end (late after next month 10th)
        # ------------------------------------------------------------------
        trips_26_end = late_trips.filtered(lambda t: t.date.day >= 26)

        for rec in trips_26_end:
            # date = next month 10th
            next_month_10 = rec.date.replace(day=1) + relativedelta(months=1)
            next_month_10 = next_month_10.replace(day=10)
            if today > next_month_10:
                rec.received_status = 'late'

    @api.onchange('invoice_id')
    def onchange_invoice_id(self):
        if self.invoice_id:
            if self.product_id and self._origin.id not in self.invoice_id.invoice_line_ids.trip_id.ids:
                # analytic_account = self.env['account.analytic.account']
                # analytic_account_name = f"{self.loading_point.name}-{self.unloading_point.name}"
                # # analytic_account_id = analytic_account.search([('name', 'ilike', analytic_account_name)], limit=1)
                # # if not analytic_account_id:
                # #     analytic_account_id = analytic_account.create({'name': analytic_account_name})
                # plan_id = self.env['account.analytic.plan'].search([('name', '=', 'Trip')], limit=1)
                # if not plan_id:
                #     plan_id = self.env['account.analytic.plan'].create({'name': 'Trip'})
                # analytic_account_id = analytic_account.create({'name': analytic_account_name, 'plan_id': plan_id.id})

                vals = {
                    'product_id': self.product_id.id,
                    'tax_ids': self.product_id.taxes_id.ids if self.product_id.taxes_id else False,
                    'price_unit': self.amount,
                    # 'analytic_account_id': analytic_account_id.id,
                    'trip_date': self.date,
                    'quantity': 1,
                    'trip_id': self._origin.id,
                    'fleet_id': self.fleet_id.id if self.fleet_id else False,
                    'dn_number': self.dn_number,
                    # 'account_id': self.company_data['default_account_revenue'].id,
                }
                if self.monthly_rent:
                    vals.update({'account_id': self.env.ref('l10n_sa.1_sa_account_500002').id})
                self.invoice_id.write({'invoice_line_ids': [(0, 0, vals)]})
            self.state = 'invoiced'

    @api.onchange('account_payment_status', 'partner_bank_ids')
    def onchange_account_payment_status(self):
        if self.account_payment_status == 'paid' and not self._origin.partner_bank_ids:
        # if self.account_payment_status == 'paid' and not self.partner_bank_ids:
            raise ValidationError(_("Can't update the payment status to Paid without Bank Details!!!"))

    # @api.constrains('account_payment_status', 'partner_bank_ids')
    # def onchange_account_payment_status(self):
    #     for trip in self:
    #         if trip.account_payment_status == 'paid' and not trip.partner_bank_ids:
    #             # if self.account_payment_status == 'paid' and not self.partner_bank_ids:
    #             raise ValidationError(_("Can't update the payment status to Paid without Bank Details!!!"))

    @api.onchange('individual_entry', 'bill_id')
    def onchange_individual_entry_and_bill_id(self):
        if self.individual_entry:
            self.account_payment_status = 'paid'
        if self.individual_entry or self.bill_id:
            self.onchange_account_payment_status()
            # if not self.account_payment_status:
            #     raise ValidationError(_("Account Payment status isn't set!!!"))
            if not self.payment_date:
                raise ValidationError(_("Payment Date isn't set!!!"))

    @api.onchange('bill_id')
    def onchange_bill_id(self):
        if self.bill_id and self.product_id and self._origin.id not in self.bill_id.invoice_line_ids.trip_id.ids:
            # analytic_account = self.env['account.analytic.account']
            # analytic_account_name = f"{self.loading_point.name}-{self.unloading_point.name}"
            # analytic_account_id = analytic_account.search([('name', '=', analytic_account_name)], limit=1)
            # if not analytic_account_id:
            #     plan_id = self.env['account.analytic.plan'].search([('name', '=', 'Trip')], limit=1)
            #     if not plan_id:
            #         plan_id = self.env['account.analytic.plan'].create({'name': 'Trip'})
            #     analytic_account_id = analytic_account.create({'name': analytic_account_name, 'plan_id': plan_id.id})
            # # analytic_account_id = analytic_account.create({'name': analytic_account_name})

            vals = {'invoice_line_ids': [(0, 0, {
                'product_id': self.product_id.id,
                'tax_ids': self.product_id.supplier_taxes_id.ids if self.product_id.supplier_taxes_id else False,
                'price_unit': self.carrier_amount,
                # 'analytic_account_id': analytic_account_id.id,
                'trip_date': self.date,
                'quantity': 1,
                'trip_id': self._origin.id,
                'fleet_id': self.fleet_id.id if self.fleet_id else False,
                'dn_number': self.dn_number,
                # 'account_id': self.company_data['default_account_revenue'].id,
            })]}
            self.bill_id.write(vals)

    def action_duplicate_trips(self):
        return {
            'name': _('Duplicate Trips'),
            'view_mode': 'form',
            'res_model': 'duplicate.trip',
            'type': 'ir.actions.act_window',
            'context': {'default_trip_id': self.id},
            'target': 'new',
        }

    @api.model
    def get_views(self, views, options=None):
        res = super().get_views(views, options)
        for view_type, view_info in res.get('views', {}).items():
            if view_type in ['form']:
                doc = etree.XML(view_info['arch'])
                if self.env.user.has_group('itruck_trip.group_can_carrier_booking_details'):
                    for field_name in ['carrier_type2', 'driver_id', 'vendor_id', 'fleet_id']:
                        for field in doc.xpath("//field[@name='%s']" % field_name):
                            if field.attrib.get('readonly'):
                                field.set('readonly', '0')
                if self.env.user.has_group('itruck_trip.group_can_edit_employee_id'):
                    for field in doc.xpath("//field[@name='employee_id']"):
                        if field.attrib.get('readonly'):
                            field.set('readonly', '0')
                if not self.env.user.has_group('itruck_trip.group_can_edit_collection_date'):
                    for field in doc.xpath("//field[@name='collection_date']"):
                        field.set('readonly', '1')

                view_info['arch'] = etree.tostring(doc, encoding='unicode')
        return res
