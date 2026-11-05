# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class NfPurchaseAdvancePaymentBill(models.TransientModel):
    _name = 'purchase.advance.payment.bill'

    advance_payment_method = fields.Selection(
    selection=[
            ('delivered', "Regular Bill"),
            ('percentage', "Down payment (percentage)"),
            ('fixed', "Down payment (fixed amount)"),
        ],
        string="Create Bill",
        default='percentage',
        required=True,
        help="A standard bill is issued with all the order lines ready for billing,"
            "according to their billing policy (based on ordered or delivered quantity).")

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        compute='_compute_currency_id',
        store=True)

    company_id = fields.Many2one(
        comodel_name='res.company',
        compute='_compute_company_id',
        store=True)

    purchase_order_ids = fields.Many2many(
        'purchase.order', default=lambda self: self.env.context.get('active_ids'))

    fixed_amount = fields.Monetary(
        string="Down Payment Amount (Fixed)",
        help="Only confirmed bills are considered.")

    amount = fields.Float(
        string="Down Payment",
        help="The percentage of amount to be Bill in advance.")

    amount_bill = fields.Monetary(
        string="Already Bill",
        currency_field='currency_id',
        help="Only confirmed down payments are considered.")

    amount_to_bill = fields.Monetary(
        string="Amount to bill",
        currency_field='currency_id',
        help="Purchase Order Total - Confirmed Bills.")

    display_draft_bill_warning = fields.Boolean(compute="_compute_display_draft_bill_warning")
    display_bill_amount_warning = fields.Boolean(compute="_compute_display_bill_amount_warning")


    @api.depends('purchase_order_ids')
    def _compute_currency_id(self):
        self.currency_id = False
        for wizard in self:
            # Fix 1: use len() instead of wizard.count
            if len(wizard.purchase_order_ids) == 1:
                wizard.currency_id = wizard.purchase_order_ids.currency_id

    @api.depends('purchase_order_ids')
    def _compute_company_id(self):
        self.company_id = False
        for wizard in self:
            # Fix 2: use len() instead of wizard.count
            if len(wizard.purchase_order_ids) == 1:
                wizard.company_id = wizard.purchase_order_ids.company_id
    
    @api.model
    def default_get(self, vals):
        res = super().default_get(vals)
        
        active_model = self.env.context.get('active_model')
        active_ids   = self.env.context.get('active_ids', [])

        if not active_model or not active_ids:
            res['amount_bill']    = 0.0
            res['amount_to_bill'] = 0.0
            return res

        purchase_orders = self.env[active_model].browse(active_ids)

        if purchase_orders:
            res['amount_bill']    = sum(purchase_orders.mapped('amount_bill'))
            res['amount_to_bill'] = sum(purchase_orders.mapped('amount_to_bill'))
        else:
            res['amount_bill']    = 0.0
            res['amount_to_bill'] = 0.0

        return res

    @api.depends('purchase_order_ids')
    def _compute_display_draft_bill_warning(self):
        for wizard in self:
            invoice_states = wizard.purchase_order_ids._origin.sudo().invoice_ids.mapped('state')
            wizard.display_draft_bill_warning = 'draft' in invoice_states

    @api.depends('amount', 'fixed_amount', 'advance_payment_method', 'amount_to_bill')
    def _compute_display_bill_amount_warning(self):
        for wizard in self:
            amount_bill = wizard.fixed_amount
            if wizard.advance_payment_method == 'percentage':
                amount_bill = wizard.amount / 100 * sum(wizard.purchase_order_ids.mapped('amount_total'))
            wizard.display_bill_amount_warning = amount_bill > wizard.amount_to_bill

    def create_bills(self):
        """Create vendor bills from selected purchase orders."""
        self.ensure_one()
        purchase_orders = self.purchase_order_ids

        if not purchase_orders:
            raise UserError(_("No purchase orders selected."))

        if self.advance_payment_method == 'delivered':
            bills = self._create_regular_bills(purchase_orders)

        elif self.advance_payment_method == 'percentage':
            if not self.amount or self.amount <= 0:
                raise UserError(_("Please enter a valid down payment percentage."))
            bills = self._create_down_payment_bills(
                purchase_orders, percentage=self.amount)

        elif self.advance_payment_method == 'fixed':
            if not self.fixed_amount or self.fixed_amount <= 0:
                raise UserError(_("Please enter a valid fixed down payment amount."))
            bills = self._create_down_payment_bills(
                purchase_orders, fixed_amount=self.fixed_amount)

        else:
            raise UserError(_("Invalid billing method."))
        
        if not bills:
            return {'type': 'ir.actions.act_window_close'}

        #  Open single bill in form view
        if len(bills) == 1:
            return {
                'type'     : 'ir.actions.act_window',
                'name'     : _('Vendor Bill'),
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id'   : bills.id,  
                'target'   : 'current',
            }

        #  Open multiple bills in list view
        return {
            'type'     : 'ir.actions.act_window',
            'name'     : _('Vendor Bills'),
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain'   : [('id', 'in', bills.ids)],
            'target'   : 'current',
        }
        

    #  Private Helpers 

    def _create_regular_bills(self, purchase_orders):
        """Create standard vendor bills for all billable order lines."""
        all_bill_vals = []

        for order in purchase_orders:
            # Check order is in valid state for billing
            if order.state not in ('purchase', 'done'):
                raise UserError(_(
                    "Purchase Order '%s' must be confirmed before creating a bill."
                ) % order.name)

            billable_lines = order.order_line.filtered(
                lambda l: not l.display_type and l.qty_received > 0
            )

            if not billable_lines:
                raise UserError(self._nothing_to_bill_error_message())

            invoice_line_vals = []

            for line in billable_lines:
                account = self._get_expense_account(line, order)

                invoice_line_vals.append((0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'quantity': line.qty_received,
                    'product_uom_id': line.uom_id.id,
                    'price_unit': line.price_unit,
                    'discount': getattr(line, 'discount', 0.0),
                    'tax_ids': [(6, 0, line.tax_ids.ids)],
                    'account_id': account.id,
                    'purchase_line_id': line.id,
                }))

            if not invoice_line_vals:
                continue

            # Bill values
            all_bill_vals.append({
                'move_type': 'in_invoice',
                'partner_id': order.partner_id.id,
                'currency_id': order.currency_id.id,
                'company_id': order.company_id.id,
                'purchase_id': order.id,
                'ref': order.name,
                'invoice_date': fields.Date.today(),
                'date': fields.Date.today(),
                'invoice_line_ids': invoice_line_vals,
            })

        # Create all bills at once
        return self.env['account.move'].create(all_bill_vals)
    
    def _get_expense_account(self, line, order):
        account = None

        # Product account
        if line.product_id:
            accounts = line.product_id.product_tmpl_id.sudo()._get_product_accounts()
            account = accounts.get('expense')

        # Category fallback
        if not account and line.product_id:
            account = line.product_id.categ_id.property_account_expense_categ_id

        # Final fallback
        if not account:
            account = self.env['account.account'].search([
                ('account_type', '=', 'expense'),
                ('company_id', '=', order.company_id.id),
                ('deprecated', '=', False),
            ], limit=1)

        # No account → error
        if not account:
            raise UserError(_(
                "No expense account found for product '%s'.\n"
                "Please configure it on the product or category."
            ) % (line.product_id.name or line.name))

        return account
    
    def _nothing_to_bill_error_message(self):
        return _(
            "Cannot create a vendor bill. No items are available to bill.\n\n"
            "To resolve this issue, please ensure that:\n"
            "   • Products have been received.\n"
            "   • Quantities to bill are greater than zero.\n"
            "   • Items are not already fully billed.\n"
        )
    
    def _create_down_payment_bills(self, purchase_orders,percentage=None, fixed_amount=None):
        """Create down payment vendor bills (percentage or fixed amount)."""
        bill_ids = []

        for order in purchase_orders:
            # Calculate down payment amount
            amount = (
                (percentage / 100.0) * order.amount_untaxed
                if percentage is not None
                else fixed_amount
            )

            account = self.env['account.account'].search([
                ('account_type', '=', 'expense'),
            ], limit=1) 
                
            today = fields.Date.today()

            if self.amount:
                line_name = _('Down Payment of %s%%') % self.amount
            else:
                line_name = _('Down Payment')
            down_payment_line = self.env['purchase.order.line'].create({
                'order_id':       order.id,
                'name':           line_name,          # temporary name
                'product_qty':    0.0,
                'price_unit':     amount,
                'date_planned':   today,
                'is_downpayment': True,
                'tax_ids':       [(5, 0, 0)],        # clear all taxes on DP line
            })
            
            
            bill = self.env['account.move'].create({
                'move_type'       : 'in_invoice',
                'partner_id'      : order.partner_id.id,
                'currency_id'     : order.currency_id.id,
                'company_id'      : order.company_id.id,
                'purchase_id'     : order.id,
                'ref'             : order.name,
                'invoice_date'    : today,
                'date' : today,
                'invoice_line_ids': [(0, 0, {
                    'name'          : line_name,
                    'quantity'      : 1,
                    'price_unit'    : amount,
                    'account_id'    : account.id if account else False,
                    'is_downpayment': True,
                    'purchase_line_id': down_payment_line.id,
                })]
            })

            
            state_label = {
                'draft':  _('Draft'),
                'posted': bill.name,   # sequence assigned on confirmation
                'cancel': _('Cancelled'),
            }.get(bill.state, bill.name or _('Unknown'))
                

            down_payment_line.write({
                'name': _('Down Payment: %s on %s') % (state_label, today),
            })
            
            bill_ids.append(bill.id)

        return self.env['account.move'].browse(bill_ids)
