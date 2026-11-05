# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, fields, api, Command, _
from odoo.exceptions import UserError
import datetime
from datetime import date, timedelta
import pytz
import calendar


def date_range(start, end):
    date_list = []
    current_date = start
    while current_date <= end:
        date_list.append(current_date.date())
        current_date += timedelta(days=1)
    return date_list

class TailorOrder(models.Model):
    _name = 'nf.tailor.order'
    _description = 'Tailor Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # This enables chatter

    name = fields.Char(string="Order Reference", required=True, copy=False, readonly=True, default='New')
    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
    order_date = fields.Date(string="Order Date", required=True, default=fields.Date.context_today)
    delivery_date = fields.Date(string="Delivery Date", required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_process', 'In Process'),
        ('delivered', 'Delivered'),
        ('cancel', 'Cancel')
    ], string="Status", default='draft', tracking=True,)
    product_id = fields.Many2one('product.product', string="Product")
    product_qty = fields.Integer(string='Quantity', default=1)
    bom_id = fields.Many2one('mrp.bom', string='Bill of Material', required=True)
    company_id = fields.Many2one(comodel_name='res.company',required=True, index=True,default=lambda self: self.env.company)
    tailor_line_ids = fields.One2many('nf.tailor.line', 'order_id', compute="_compute_tailor_line_ids", store=True, readonly=False,copy=False,)
    measurement_line_ids = fields.One2many('nf.measurement.line', 'tailor_order_id', compute="_compute_measurement_lines", store=True, readonly=False,copy=False,tracking=True,)
    design_ids = fields.One2many('nf.measurement.design', 'tailor_order_id', compute="_compute_measurement_design_lines", store=True, readonly=False,copy=False,tracking=True,)
    measurement_id = fields.Many2one('nf.measurement', string="Measurement")
    manufacturing_order_id = fields.Many2one( 'mrp.production', string='Manufacturing Order', )
    sale_order_id = fields.Many2one('sale.order', string="Sale order")
    sale_order_count  = fields.Integer('sale count', compute="_compute_sale_order_count")
    manufacturing_order_count  = fields.Integer('manufacturing count', compute="_compute_manufacturing_order_count")
    picking_count  = fields.Integer('Picking count', compute="_compute_picking_count")
    
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        compute='_compute_currency_id',
        store=True,
        precompute=True,
        ondelete='restrict'
    )
    amount_untaxed = fields.Monetary(related='sale_order_id.amount_untaxed')
    amount_tax = fields.Monetary(related='sale_order_id.amount_tax')
    amount_total = fields.Monetary(related='sale_order_id.amount_total')
    
    @api.model
    def nf_open_invoice(self, invoice_id):
        return {
            'name': _('Invoice'),
            'res_id': invoice_id,
            'view_mode': 'form',
            'res_model': 'account.move',
            'views': [[False, "form"]],
            'type': 'ir.actions.act_window',
            'target': 'new'
        }

    @api.model
    def get_pending_deliverys(self,start_date, end_date):
        StartDate =  datetime.datetime.strptime(start_date, "%Y-%m-%d")
        EndDate =   datetime.datetime.strptime(end_date, "%Y-%m-%d") 
        pending_delievery = self.search([('order_date','>=',StartDate),('order_date','<=',EndDate),('state','=','in_process')])
        pending_delievery_list = []
        if pending_delievery:
            pending_delievery_list = pending_delievery.read(['id','name','customer_id','order_date','delivery_date']) or []

        return pending_delievery_list

    @api.model 
    def get_invoice_model(self, start_date, end_date, Filter):
        today = date.today()
        res_pos_order = {}
        StartDate =  datetime.datetime.strptime(start_date, "%Y-%m-%d")
        EndDate =   datetime.datetime.strptime(end_date, "%Y-%m-%d") 
        if Filter == 'day':
            list1 = []
            Orders = self.env['account.move'].search_read([('invoice_date','=', today)], ['invoice_date', 'amount_total'])
            hour_list = []
            total_by_date = {'hour': 0, 'amount': 0.00}
            final_dict = {}
            for order in Orders:
                user_tz = pytz.timezone(self.env.user.tz or 'UTC')
                local_dt = datetime.datetime.now(user_tz)
                hour = local_dt.hour

                if hour in hour_list:
                    total_by_date.update({'hour': hour, 'amount': total_by_date.get(
                        'amount') + order.get('amount_total')})
                else:
                    total_by_date.update(
                        {'hour': hour, 'amount': order.get('amount_total')})

                if hour in final_dict:
                    final_dict[hour] = (
                        {'hour': hour, 'amount': '%.2f' % total_by_date.get('amount') or 0})
                else:
                    final_dict[hour] = {
                        'hour': 0, 'amount': '%.2f' % total_by_date.get('amount') or 0}
                hour_list.append(hour)

            hour_lst = [hrs for hrs in range(0, 24)]
            for hrs in hour_lst:
                hr = []
                if hrs != 23:
                    hr += [hrs, hrs + 1]
                else:
                    hr += [hrs, 0]
                if hour_lst[hrs] in hr:
                    if (final_dict.get(hour_lst[hrs])):
                        list1.append({'time': hr, 'orderTotal': final_dict.get(
                            hour_lst[hrs]).get('amount')})
                    else:
                        list1.append({'time': hr, 'orderTotal': 0.00})
            res_pos_order['Sales_Data'] = list1

        elif Filter == 'month':
            monthData = []
            for MonthDate in date_range(StartDate, EndDate):
                Invoices = self.env['account.move'].search([('invoice_date','=', MonthDate)])
                DayTotalSale = sum(Invoices.mapped('amount_total'))
                monthData.append({'day': str(MonthDate.day)+'-'+ str(MonthDate.month)+'-' + str(MonthDate.year) , 'Amount': '%.2f' % DayTotalSale})
            res_pos_order['Sales_Data'] = monthData

        elif Filter == 'year':
            monthlist = ['jan', 'feb', 'mar', 'apr', 'may',
                         'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
            monthData = []
            tempDate = date(today.year, 1, 1)
            for monthCount in range(1, len(monthlist) + 1):
                StatDate = tempDate.replace(month=monthCount)
                EndDate = StatDate.replace(day=calendar.monthrange(today.year, monthCount)[1])
                if monthCount == StatDate.month:
                    monthData.append({'month': monthlist[monthCount - 1], 'Amount': '%.2f' % sum(self.env['account.move'].search(
                        [('invoice_date', '>=', str(StatDate)), ('invoice_date', '<=', str(EndDate))]).mapped('amount_total'))})
                else:
                    monthData.append(
                        {'month': monthlist[monthCount - 1], 'Amount': 0.00})

            res_pos_order['Sales_Data'] = monthData

        return res_pos_order


    @api.model
    def get_gender_data_fom_model(self, start_date, end_date, base):
        today = date.today()
        StartDate =  datetime.datetime.strptime(start_date, "%Y-%m-%d")
        EndDate =   datetime.datetime.strptime(end_date, "%Y-%m-%d")
        if base == 'day':
            total_orders = self.search([('order_date','=', today)])
        elif base =='year' :
            total_orders = self.search([('order_date','<=', EndDate), ('order_date', '>=', StartDate)])
        else:
            total_orders = self.search([('order_date','<=', EndDate), ('order_date', '>=', StartDate)])
        
        male_count = len(total_orders.filtered(lambda r: r.measurement_id and r.measurement_id.gender == 'male'))
        female_count = len(total_orders.filtered(lambda r: r.measurement_id and r.measurement_id.gender == 'female'))
        other_count = len(total_orders.filtered(lambda r: r.measurement_id and r.measurement_id.gender == 'other'))
        gender_count = [{'gender': 'Male', 'count': male_count}, {'gender': 'Female', 'count': female_count}, {'gender': 'Other', 'count': other_count}]

        return gender_count

    @api.model
    def get_counter_card_details(self, start_date, end_date):
        user = self.env.user.read()[0]
        StartDate =  datetime.datetime.strptime(start_date, "%Y-%m-%d")
        EndDate =  datetime.datetime.strptime(end_date, "%Y-%m-%d")
        total_orders = self.search([('order_date','<=', EndDate), ('order_date', '>=', StartDate)])

        total_order_count = 0
        inprogres_orders_count = 0
        new_orders_count = 0
        confirmed_orders = 0
        done_orders = 0
        cancel_orders = 0
        
        amount_list = []
        gender_count = []
        pending_delievery_list = []
        invoice_list = []
        recent_customer_list = []  
        delievered_order_list = []
        if total_orders:
            total_order_count = len(total_orders)
            inprogres_orders_count =  len(total_orders.filtered(lambda x: x.state == 'in_process'))
            new_orders_count =  len(total_orders.filtered(lambda x: x.state == 'draft'))
            new_orders_count =  len(total_orders.filtered(lambda x: x.state == 'draft'))
            done_orders =  len(total_orders.filtered(lambda x: x.state == 'delivered'))
            confirmed_orders =  len(total_orders.filtered(lambda x: x.state == 'confirmed'))
            cancel_orders =  len(total_orders.filtered(lambda x: x.state == 'cancel'))
            
            # Count by gender
            male_count = len(total_orders.filtered(lambda r: r.measurement_id and r.measurement_id.gender == 'male'))
            female_count = len(total_orders.filtered(lambda r: r.measurement_id and r.measurement_id.gender == 'female'))
            other_count = len(total_orders.filtered(lambda r: r.measurement_id and r.measurement_id.gender == 'other'))

            gender_count = [{'gender': 'Male', 'count': male_count}, {'gender': 'Female', 'count': female_count}, {'gender': 'Other', 'count': other_count}]

            
            if total_orders:
                amount_list = total_orders.tailor_line_ids.mapped('unit_price')

            pending_delievery = self.search([('order_date','>=',StartDate),('order_date','<=',EndDate),('state','=','in_process')], limit=10)
            
            if pending_delievery:
                pending_delievery_list = pending_delievery.read(['id','name','customer_id','order_date','delivery_date']) or []
            
            delievered_order = self.search([('order_date','>=',StartDate),('order_date','<=',EndDate),('state','=','delivered')], limit=10)
            
            if delievered_order:
                delievered_order_list = delievered_order.read(['name','customer_id','order_date','delivery_date']) or []
            
            confirmed_order = self.search([('order_date','>=',start_date),('order_date','<=',end_date),('state','=','confirmed')], limit=10)
            if confirmed_order or delievered_order or delievered_order:
                partner_ids = []
                for total_selling_order in total_orders:
                    if len(partner_ids) <= 10:
                        if total_selling_order.customer_id.id not in partner_ids:
                            customer_details = self.env["res.partner"].browse(total_selling_order.customer_id.id)
                            customer =  customer_details.read(['name','phone'])
                            recent_customer_list.append({
                                'recent_customer' :customer,
                                'order_creation_date': total_selling_order.order_date
                            })
                    partner_ids.append(total_selling_order.customer_id.id)

            invoice_list = self.env['account.move'].search([('payment_state','=', 'partial')], limit=10).read([ 'name', 'amount_total', 'amount_residual',])
        return {
            'user':user, 
            'sale_amount': sum(amount_list),
            'total_order_count': total_order_count,
            'inprogres_orders_count':inprogres_orders_count,
            'new_orders_count':new_orders_count,
            'confirmed_orders':confirmed_orders,
            'done_orders':done_orders,
            'cancel_orders':cancel_orders,
            'gender_count':gender_count,
            'pending_delievery_list': pending_delievery_list,
            'recent_customer_list': recent_customer_list,
            'invoice_list': invoice_list,
            'delievered_order_list': delievered_order_list,
        }
    
    
    def action_cancel(self):
        self.ensure_one()

        if self.state in ('delivered', 'cancel'):
            raise UserError(_("A delivered or already cancelled order cannot be modified."))

        cancellation_log = [_("Tailor Order cancellation process started.")]

        # 1. Cancel related Manufacturing Order first (if it exists)
        if self.manufacturing_order_id and self.manufacturing_order_id.state != 'cancel':
            mo_to_cancel = self.manufacturing_order_id
            if mo_to_cancel.state != 'cancel':
                mo_to_cancel.action_cancel()
                cancellation_log.append(_("Related Manufacturing Order %s was cancelled.", mo_to_cancel.name))

        # 2. Handle the Sale Order and its related Invoices and Deliveries
        if self.sale_order_id and self.sale_order_id.state != 'cancel':
            sale_order = self.sale_order_id
            
            # Find and cancel any linked invoices
            if sale_order.invoice_ids:
                for invoice in sale_order.invoice_ids.filtered(lambda inv: inv.state != 'cancel'):
                    if invoice.state == 'posted':
                        invoice.button_draft()
                    invoice.button_cancel()
                    cancellation_log.append(_("Related Invoice %s was cancelled.", invoice.name))

            # Find and cancel any linked Deliveries (Stock Pickings)
            if sale_order.picking_ids:
                for picking in sale_order.picking_ids.filtered(lambda p: p.state != 'cancel'):
                    if picking.state == 'done':
                        raise UserError(
                            _("Cannot cancel this order. At least one delivery (%s) has already been validated. "
                              "Please reverse the delivery first.", picking.name)
                        )
                    picking.action_cancel()
                    cancellation_log.append(_("Related Delivery %s was cancelled.", picking.name))

            
            sale_order.with_context(mail_notrack=True).action_cancel()
            cancellation_log.append(_("Related Sale Order %s was cancelled (Customer notification skipped).", sale_order.name))

        # 3. Finally, set the Tailor Order's state to 'cancel'
        self.write({'state': 'cancel'})
        cancellation_log.append(_("Tailor Order is now Cancelled."))

        # Post the full log to the chatter
        self.message_post(body="<br/>".join(cancellation_log))

        return True

    @api.depends('company_id')
    def _compute_currency_id(self):
        for order in self:
            order.currency_id = order.company_id.currency_id

    def _compute_sale_order_count(self):
        for order in self:
            order.sale_order_count = len(order.sale_order_id.ids)
    def _compute_manufacturing_order_count(self):
        for order in self:
            order.manufacturing_order_count = len(order.manufacturing_order_id.ids)
    def _compute_picking_count(self):
        for order in self:
            order.picking_count = len(order.sale_order_id.picking_ids.ids)

    def nf_deliver_order(self):
        self.message_post(body=_("Order Delivered."))


    def action_view_sales_orders(self):
        action = {
            'name': _('Sales Order(s)'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'target': 'current',
        }
        sale_order_ids = self.sale_order_id.ids
        if len(sale_order_ids) == 1:
            action['res_id'] = sale_order_ids[0]
            action['view_mode'] = 'form'
        else:
            action['view_mode'] = 'list,form'
            action['domain'] = [('id', 'in', sale_order_ids)]
        return action

    def action_view_picking_orders(self):
        action = {
            'name': _('Delivery Order(s)'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'target': 'current',
        }
        picking_ids = self.sale_order_id.picking_ids.ids
        if len(picking_ids) == 1:
            action['res_id'] = picking_ids[0]
            action['view_mode'] = 'form'
        else:
            action['view_mode'] = 'list,form'
            action['domain'] = [('id', 'in', picking_ids)]
        return action

    def action_view_manufacturing_orders(self):
        action = {
            'name': _('Manufacturing Order(s)'),
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production',
            'target': 'current',
        }
        manufacturing_order_ids = self.manufacturing_order_id.ids
        if len(manufacturing_order_ids) == 1:
            action['res_id'] = manufacturing_order_ids[0]
            action['view_mode'] = 'form'
        else:
            action['view_mode'] = 'list,form'
            action['domain'] = [('id', 'in', manufacturing_order_ids)]
        return action

    @api.depends('measurement_id')
    def _compute_measurement_lines(self):
        for record in self:
            record.measurement_line_ids = [Command.clear()] + [Command.create(line_vals) for line_vals in record.measurement_id.measurement_line_ids.read(load=False)]
        
    @api.depends('measurement_id')
    def _compute_measurement_design_lines(self):
        for record in self:
            record.design_ids = [Command.clear()] + [Command.create(line_vals) for line_vals in record.measurement_id.measurement_design_ids.read(load=False)]

    @api.depends('product_qty', 'bom_id')
    def _compute_tailor_line_ids(self):
        for record in self:
            components = record
            print("\n\n\n\n components ???")
            for line in record:
                print("\n\n\n\n line ???",line.product_qty)
                print("\n\n\n\n record ???",record.product_qty)
            record.tailor_line_ids = [Command.clear()] + [Command.create({
                    'product_id':line.product_id.id,
                    'quantity': line.product_qty * record.product_qty,
                    'uom_id': line.uom_id.id if line.product_id.type != 'service' else False,
                }) for line in record.bom_id.bom_line_ids]
                
    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if val.get('name', 'New') == 'New':
                val['name'] = self.env['ir.sequence'].next_by_code('nf.tailor.order.sequence') or 'New'
        res = super().create(vals)
        for record in res:
            if record.customer_id:
                record.message_subscribe([record.customer_id.id])
        return res
    
    def write(self, vals):
        result = super(TailorOrder, self).write(vals)
        # if self.customer_id and self.customer_id not in self.message_follower_ids:
        #     self.message_subscribe([self.customer_id.id])
        
        return result
    

    def nf_create_so(self):
        sale_order_values_list = [{
                "company_id": self.company_id.id,
                "partner_id": self.customer_id.id,
                'tailor_order_id': self.id,
                "order_line":  [Command.create({
                    'name':self.bom_id.product_id.name,
                    'product_id':self.bom_id.product_id.id,
                    'product_uom_qty': self.product_qty,
                    'product_uom_id': self.bom_id.product_id.uom_id.id,
                })] +[Command.create({
                    'name': line.product_id.name,
                    'product_id':line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'product_uom_id': line.product_id.uom_id.id if not line.uom_id else line.uom_id.id,
                }) for line in self.tailor_line_ids],
            }]
        sale_order =  self.env['sale.order'].create(sale_order_values_list)
        
        self.sale_order_id = sale_order.id
        self.state = "confirmed"
        self.message_post(body=_("Order confirmed."))

    @api.model
    def _get_default_picking_type_id(self, company_id):
        return self.env['stock.picking.type'].search([
            ('code', '=', 'mrp_operation'),
            ('warehouse_id.company_id', '=', company_id),
        ], limit=1).id

    def nf_create_mo(self):
        moObj = self.env['mrp.production'].create({
            'product_id': self.bom_id.product_id.id,
            'bom_id': self.bom_id.id,
            'picking_type_id': self._get_default_picking_type_id(self.company_id.id),
            'product_qty': self.product_qty,
            'tailor_order_id': self.id,
            'uom_id': self.bom_id.product_id.uom_id.id,
            'user_id': self.env.user.id,
            'origin': ",".join(sorted([production.name for production in self])),
            'move_raw_ids': [Command.create({'product_id':val.product_id.id, 'product_uom_qty':val.quantity}) for val in self.tailor_line_ids]
        })

        self.manufacturing_order_id = moObj.id
        self.state = "in_process"
        self.message_post(body=_("Manufacture Order Created."))
