# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import fields,models,api
import datetime
from datetime import date,datetime,timedelta,time
import calendar
import pytz

def date_range(start, end):
        date_list = []
        current_date = start
        while current_date <= end:
            date_list.append(current_date.date())
            current_date += timedelta(days=1)
        return date_list
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def sale_Order_Record(self):  
        user_id = self.env.user
        user_details = user_id.read(["id","name","currency_id"])
        amount_total = 0
        current_date = datetime.today()
        current_year = current_date.year
        current_month = current_date.month
        today_start_time = datetime.combine(current_date,datetime.min.time())
        today_end_time = datetime.combine(current_date,datetime.max.time())
        month_number_of_days = calendar.monthrange(current_year,current_month)
        current_month_first_date = current_date.replace(day=1)
        current_month_last_date = current_date.replace(day=month_number_of_days[1])
        current_month_first_date_start_time = datetime.combine(current_month_first_date,datetime.min.time())
        current_month_first_date_end_time = datetime.combine(current_month_last_date,datetime.min.time())
        
        today_highest_sale_amount = 0
        month_heighest_sale_amount= 0
        average_amount_total = 0
        average_amount = 0
        
        records = self.search([])
        today_top_sale = self.search([("date_order",">=",today_start_time),("date_order","<=",today_end_time)])
        month_top_sale = self.search([("date_order",">=",current_month_first_date_start_time),("date_order","<=",current_month_first_date_end_time)])
        
        for today_amount_record in today_top_sale:
            if today_amount_record.amount_total > today_highest_sale_amount:
                today_highest_sale_amount = today_amount_record.amount_total
        
        for month_amount_record in month_top_sale:
            if month_amount_record.amount_total > month_heighest_sale_amount:
                month_heighest_sale_amount = month_amount_record.amount_total     
        
        for record in records:
            if amount_total < record.amount_total:
                amount_total = record.amount_total
            
        for record in records:
            average_amount_total += record.amount_total
        average_amount = average_amount_total / len(records)
            
        return{
            "user_details_obj":user_details,
            "today_highest_sale_object":today_highest_sale_amount,
            "todays_heightest_amount_obj":amount_total,
            "month_heighest_sale_amount_obj":month_heighest_sale_amount,
            "month_total_sale_obj":len(month_top_sale),
            "average_amount_obj":round(average_amount,2),
        }
        
    @api.model 
    def nf_get_sales_data(self,start_date,end_date,sales_filter):
        current_date = datetime.today()
        current_year = current_date.year
        current_month = current_date.month
        month_number_of_days = calendar.monthrange(current_year,current_month)
        current_month_last_date = current_date.replace(day=month_number_of_days[1])
        today = date.today()
        today_start = datetime.combine(fields.Date.today(), time.min)
        today_end = datetime.combine(fields.Date.today(), time.max)
        res_pos_order = {}
        startdate = datetime.strptime(start_date, "%Y-%m-%d")
        enddate = datetime.strptime(end_date, "%Y-%m-%d")
        if sales_filter == "today":
            list1 = []
            
            orders = self.search_read([("date_order", ">=", today_start),
        ("date_order", "<=", today_end),],["date_order","amount_total"])
            hour_list = []
            total_by_date = {'hour': 0, 'amount': 0.00}
            final_dict = {}
            for order in orders:
                user_tz = pytz.timezone(self.env.user.tz or 'UTC')
                local_dt = datetime.now(user_tz)
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
            res_pos_order['sales_record'] = list1
        elif sales_filter == 'month':
            monthData = []
            for MonthDate in date_range(startdate, current_month_last_date):
                date_start = datetime.combine(MonthDate, time.min)
                date_end = datetime.combine(MonthDate, time.max)
                orders = self.search([('date_order','>=', date_start),('date_order',"<=",date_end)])
                DayTotalSale = sum(orders.mapped('amount_total'))
                monthData.append({'day': str(MonthDate.day)+'-'+ str(MonthDate.month)+'-' + str(MonthDate.year) , 'Amount': '%.2f' % DayTotalSale})
            res_pos_order['sales_record'] = monthData
            
        elif sales_filter == 'year':
            monthlist = ['jan', 'feb', 'mar', 'apr', 'may',
                         'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
            yearData = []
            tempdate = date(today.year, 1, 1)
            for monthCount in range(1, len(monthlist) + 1):
                yearstartdate = tempdate.replace(month=monthCount)
                yearenddate = yearstartdate.replace(day=calendar.monthrange(today.year, monthCount)[1])
                yearstartdatewithtime = datetime.combine(yearstartdate, time.min)
                yearenddatewithtime = datetime.combine(yearenddate, time.max)
                if monthCount == yearstartdate.month:
                    yearData.append({'month': monthlist[monthCount - 1], 'Amount': '%.2f' % sum(self.search(
                        [('date_order', '>=', yearstartdatewithtime), ('date_order', '<=', yearenddatewithtime)]).mapped('amount_total'))})
                else:
                    yearData.append(
                        {'month': monthlist[monthCount - 1], 'Amount': 0.00})

            res_pos_order['sales_record'] = yearData
        
        return res_pos_order
            
    def monthly_Sale_Order_Record(self):
        current_date = datetime.today()
        current_year = current_date.year
        current_month = current_date.month
        month_number_of_days = calendar.monthrange(current_year,current_month)
        current_month_first_date = current_date.replace(day=1)
        current_month_last_date = current_date.replace(day=month_number_of_days[1])
        range_of_month = current_month_last_date.day
        i=1
        for _ in range(range_of_month):
            monthly_record_set = {
            
            }
            i += 1

    def top_Sale_Order_Record(self,start_date,end_date):
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        start_time = datetime.combine(start_date_obj,datetime.min.time())
        end_time = datetime.combine(end_date_obj,datetime.max.time())
        sale_orders = self.search([('date_order','>=', start_time),('date_order',"<=",end_time)]).sorted("amount_total",reverse=True)
        invoice_sale_orders = self.search([])
        top_sale_order_list = []
        top_sale_order_dict = {}
        nf_invoice_due_list = []
        running_sale_order_list = []
        id_store = []
        top_sale_order = 0
        # product_total_quantity = 0
        
        for record in sale_orders:
            top_sale_order_dict = {
                "id": record.id,
                "sale_order_number":record.name,
                "sale_order_customer":record.partner_id.name,
                "sales_person": record.user_id.name,
                "Total":record.amount_total,
                "product_quantity":0
            }
            product_total_quantity = sum(
                record.order_line.mapped('product_uom_qty')
            )
                
            top_sale_order_dict["product_quantity"] = product_total_quantity
            top_sale_order_list.append(top_sale_order_dict)
            
        for order in invoice_sale_orders:
            if start_time <= order.date_order <= end_time and order.state in ["draft","sent"]:
                running_sale_order_list.append(
                    {
                        "order_name":order.display_name,
                        "partner_name":order.partner_id.display_name,
                        "create_date":order.create_date,
                        "order_date":order.date_order
                    }
                )
            
            for invoice in order.invoice_ids:
                if invoice.invoice_date and start_date_obj <= invoice.invoice_date <= end_date_obj:
                    nf_invoice_due_list.append(
                        {
                            "invoice_number":invoice.display_name,
                            "amount":invoice.amount_total,
                            "amount_due":invoice.amount_residual,
                        }
                    )
        return {
            "sale_order_object":top_sale_order_list or [],
            "invoice_due_obj":nf_invoice_due_list or [],
            "running_sale_order_obj":running_sale_order_list or [],
        }
    
    def top_Selling_Product(self,start_date,end_date):
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        start_time = datetime.combine(start_date_obj,datetime.min.time())
        end_time = datetime.combine(end_date_obj,datetime.max.time())
        top_products = self.env['sale.order.line']._read_group(
            domain=[
                ('order_id.state', '=', 'sale'),("order_id.date_order",">=",start_time),("order_id.date_order","<=",end_time)
            ],
            groupby=['product_id'],
            aggregates=[
                'product_uom_qty:sum',
                'price_total:sum',
            ],
            limit=10,
        )
        top_products = sorted(
            top_products,
            key=lambda x: x[1] or 0,
            reverse=True
        )
        
        top_product_list = []
        
        for product, qty_sum, total_sum in top_products:
            top_product_list.append({
                'product_name': product.display_name,
                'sale_qty': qty_sum,
                'total': total_sum,
            })
        
        return {
            "top_product_obj":top_product_list
        }
        
    def top_customer_by_revenue(self,start_date,end_date):
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        start_time = datetime.combine(start_date_obj,datetime.min.time())
        end_time = datetime.combine(end_date_obj,datetime.max.time())
        top_customer_list = []
        
        top_customers = self._read_group(
            domain=[
                ("state","=","sale"),("date_order",">=",start_time),("date_order","<=",end_time)
            ],
            groupby=["partner_id"],
            aggregates=[
            'amount_total:sum'    
            ],
            limit=10,
        )
        
        top_customers = sorted(
            top_customers,
            key=lambda x:x[1] or 0,
            reverse=True
        )
        
        for customer,amount in top_customers:
            top_customer_list.append({
                "customer_name":customer.name,
                "amount":amount
            })

        return {
            "top_customer_record":top_customer_list
        }
        
    def pending_sale_orders(self,start_date,end_date):
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        start_time = datetime.combine(start_date_obj,datetime.min.time())
        end_time = datetime.combine(end_date_obj,datetime.max.time())
        picking_sale_orders = self.search([('picking_ids', '!=', False),("date_order",">=",start_time),("date_order","<=",end_time)])
        pending_delivery_orders_list = []
        state_label = dict(self.env['stock.picking'].fields_get(allfields=['state'])['state']['selection'])
        
        for order in picking_sale_orders:
            for picking in order.picking_ids:
                if picking.state in ('draft','waiting','confirmed','assigned'):
                    pending_delivery_orders_list.append({
                        "name":picking.display_name,
                        "scheduled_date":picking.scheduled_date,
                        "state": state_label.get(picking.state)
                    })
        return {
            "pending_delivery_order_obj":pending_delivery_orders_list,
        }