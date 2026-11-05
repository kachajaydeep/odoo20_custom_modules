# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.
  
from odoo import models, fields, api
import calendar
from datetime import datetime, date, timedelta
import pytz


def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days


def start_end_date_by_time_zone(start, end, tz):
    tz = pytz.timezone(tz) or 'UTC'
    current_time = datetime.now(tz)
    hour_tz = int(str(current_time)[-5:][:2])
    min_tz = int(str(current_time)[-5:][3:])
    sign = str(current_time)[-6][:1]
    sdate = start + " 00:00:00"
    edate = end + " 23:59:59"
    if sign == '-':
        start_date = (datetime.strptime(sdate, '%Y-%m-%d %H:%M:%S') +
                      timedelta(hours=hour_tz, minutes=min_tz)).strftime("%Y-%m-%d %H:%M:%S")
        end_date = (datetime.strptime(edate, '%Y-%m-%d %H:%M:%S') +
                    timedelta(hours=hour_tz, minutes=min_tz)).strftime("%Y-%m-%d %H:%M:%S")
    if sign == '+':
        start_date = (datetime.strptime(sdate, '%Y-%m-%d %H:%M:%S') -
                      timedelta(hours=hour_tz, minutes=min_tz)).strftime("%Y-%m-%d %H:%M:%S")
        end_date = (datetime.strptime(edate, '%Y-%m-%d %H:%M:%S') -
                    timedelta(hours=hour_tz, minutes=min_tz)).strftime("%Y-%m-%d %H:%M:%S")
    return start_date, end_date


class NfPosDashboard(models.Model):
    _name = "nf.pos.dashboard"
    _description = 'Model is use for design'

    name = fields.Char(string="Name")

    @api.model
    def get_current_user(self):
        return self.env.user.read()[0]

    @api.model
    def get_all_pos_order_data(self, company_id): 
        print('\n\n\n company_id', company_id)
        Today = datetime.today().strftime('%Y-%m-%d')
        today = fields.Date.today()
        Active_sessions = self.env['pos.session'].search(
            [('state', 'in', ['opened', 'opening_control'])])
        current_time_zone = self.env.user.tz or 'UTC'
        start_date, end_date = start_end_date_by_time_zone(
            Today, Today, current_time_zone)

        MonthStartDate = today.replace(day=1)
        MonthEndDate = today.replace(
            day=calendar.monthrange(today.year, today.month)[1])

        # calculate Total pos sales and total products sold from pos
        today_sales_query = """SELECT SUM(pol.price_subtotal_incl) AS today_sales_total, MAX(pol.price_subtotal_incl) AS max_order_total,  SUM (pol.qty) AS today_product_sold FROM pos_order as po INNER JOIN pos_order_line AS pol ON po.id = pol.order_id WHERE po.date_order >= '%s' AND po.date_order <= '%s' AND po.company_id = %s""" % (
            start_date, end_date, company_id)

        heights_month_sale = """SELECT MAX(po.amount_total) AS heights_month_sale, sum(pol.price_subtotal_incl) AS month_sale, ROUND(SUM(pol.price_subtotal_incl) / SUM(pol.qty), 2) AS avrage_salling_amount FROM pos_order as po INNER JOIN pos_order_line AS pol ON po.id = pol.order_id WHERE po.date_order >= '%s' AND date(po.date_order) <= date('%s') AND po.company_id = %s""" % (MonthStartDate, MonthEndDate, company_id)

        self._cr.execute(heights_month_sale)
        heights_month_sale = self._cr.dictfetchall()

        self._cr.execute(today_sales_query)
        Today_total_sale = self._cr.dictfetchall() 
        return {
            'Today_total_sale': Today_total_sale[0].get('today_sales_total') or 0.00,
            'today_product_sold': Today_total_sale[0].get('today_product_sold'),
            'Total_active_sessions': len(Active_sessions),
            'max_order_total': Today_total_sale[0].get('max_order_total') or 0.00,
            'currency_symbol': self.env.user.currency_id.symbol,
            'heights_month_sale': heights_month_sale[0].get('heights_month_sale'),
            'month_sale': heights_month_sale[0].get('month_sale'),
            'avrage_salling_amount': heights_month_sale[0].get('avrage_salling_amount')
        }

    @api.model
    def get_moth_sale_data_for_chart(self, start, end, Filter, company_id):
        res_pos_order = {}
        today = fields.Date.today()

        if Filter == 'Day':
            list1 = []
            Orders = self.env['pos.order'].search_read([('date_order', '<=', str(
                today)), ('date_order', '>=', str(today)), ('company_id', '=', company_id)], ['date_order', 'amount_total'])

            hour_list = []
            total_by_date = {'hour': 0, 'amount': 0.00}
            final_dict = {}

            for order in Orders:
                hour = order.get('date_order').astimezone(
                    pytz.timezone(self.env.user.tz or 'UTC')).hour

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

        elif Filter == 'Month':
            MonthStartDate = today.replace(day=1)
            MonthEndDate = today.replace(
                day=calendar.monthrange(today.year, today.month)[1])
            monthData = []
            for MonthDate in date_range(MonthStartDate, MonthEndDate):
                DayTotalSale = sum(self.env['pos.order'].search([('date_order', '<=', str(
                    MonthDate)), ('date_order', '>=', str(MonthDate)), ('company_id', '=', company_id)]).mapped('amount_total'))
                monthData.append(
                    {'day': str(MonthDate.day)+'-'+ str(today.month)+'-' + str(today.year) , 'Amount': '%.2f' % DayTotalSale})

            res_pos_order['Sales_Data'] = monthData

        elif Filter == 'Year':
            monthlist = ['jan', 'feb', 'mar', 'apr', 'may',
                         'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
            monthData = []

            tempDate = date(today.year, 1, 1)

            for monthCount in range(1, len(monthlist) + 1):
                StatDate = tempDate.replace(month=monthCount)
                EndDate = StatDate.replace(
                    day=calendar.monthrange(today.year, monthCount)[1])
                if monthCount == StatDate.month:
                    monthData.append({'month': monthlist[monthCount - 1], 'Amount': '%.2f' % sum(self.env['pos.order'].search(
                        [('date_order', '>=', str(StatDate)), ('date_order', '<=', str(EndDate))]).mapped('amount_total'))})
                else:
                    monthData.append(
                        {'month': monthlist[monthCount - 1], 'Amount': 0.00})

            res_pos_order['Sales_Data'] = monthData

        res_pos_order['Currency_symbol'] = self.env.user.currency_id.symbol
        return res_pos_order

    @api.model
    def getSaleProductDate(self, company_id):
        today = fields.Date.today()
        MonthStartDate = today.replace(day=1)
        MonthEndDate = today.replace(
            day=calendar.monthrange(today.year, today.month)[1])
        sql_query = """SELECT 
                        SUM(pol.price_subtotal_incl) AS totalamount, 
                        pt.name AS product_name,
                        SUM(pol.qty) AS total_qty , pp.id AS product_id
                        FROM pos_order_line AS pol
                        INNER JOIN pos_order AS po ON po.id = pol.order_id
                        INNER JOIN product_product AS pp ON pol.product_id=pp.id
                        INNER JOIN product_template AS pt ON pt.id=pp.product_tmpl_id
                        WHERE po.date_order >= '%s'
                        AND po.company_id = %s
                        GROUP BY product_name, pp.id
                        ORDER BY totalamount DESC LIMIT 10
                    """ % (today, company_id)
        self._cr.execute(sql_query)
        result_top_product = self._cr.dictfetchall()
        data_source = []
        count = 0
        for each in result_top_product:
            count += 1
            data_source.append(['<strong>' + str(count) + '</strong>', each.get('product_name'), str(each.get('total_qty')),
                                str(self.env.user.currency_id.symbol+" "+"%.2f" % each.get('totalamount'))])
        return data_source

    @api.model
    def get_top_customer_data(self, company_id):
        today = fields.Date.today()
        MonthStartDate = today.replace(day=1)
        MonthEndDate = today.replace(day=calendar.monthrange(today.year, today.month)[1])
        sql_query = """ SELECT SUM(pol.price_subtotal_incl) AS Amount, partner.name AS partner_name, SUM(pol.qty) AS total_product
                            FROM pos_order_line AS pol 
                            INNER JOIN pos_order AS po ON po.id = pol.order_id 
                            INNER JOIN res_partner AS partner ON partner.id = po.partner_id
                            where po.date_order >= '%s' 
                            AND date(po.date_order) <= date('%s') 
                            AND po.company_id = %s
                            GROUP BY partner.name ORDER BY Amount DESC LIMIT 7 """ % (MonthStartDate, MonthEndDate, company_id)
        self._cr.execute(sql_query)
        PartnerData = self._cr.dictfetchall()

        return {'PartnerData': PartnerData, 'currency_symbol': self.env.user.currency_id.symbol,}

    @api.model
    def GetThisMonthPaymentData(self, company_id):
        today = fields.Date.today()
        MonthStartDate = today.replace(day=1)
        MonthEndDate = today.replace(day=calendar.monthrange(today.year, today.month)[1])
        
        sql_query = """ SELECT SUM(pospayment.amount) AS Amount, ppm.name AS payment_name
                            FROM pos_payment AS pospayment
                            INNER JOIN pos_payment_method AS ppm ON ppm.id = pospayment.payment_method_id 
                            where pospayment.payment_date >= '%s' 
                            AND date(pospayment.payment_date) <= date('%s') 
                            AND pospayment.company_id = %s
                            GROUP BY ppm.name """ % (MonthStartDate, MonthEndDate, company_id)
        self._cr.execute(sql_query)
        PaymentData = self._cr.dictfetchall()
        return PaymentData

    @api.model
    def GetStockData(self, company_id):
        today = fields.Date.today()
        MonthStartDate = today.replace(day=1)
        MonthEndDate = today.replace(day=calendar.monthrange(today.year, today.month)[1])

        sql_query = """SELECT 
                        SUM(pol.price_subtotal_incl) AS totalamount, 
                        pt.name AS product_name,
                        SUM(pol.qty) AS total_qty, pp.id AS product_id
                        FROM pos_order_line AS pol
                        INNER JOIN pos_order AS po ON po.id = pol.order_id
                        INNER JOIN product_product AS pp ON pol.product_id=pp.id
                        INNER JOIN product_template AS pt ON pt.id=pp.product_tmpl_id
                        WHERE po.date_order >= '%s'
                        AND po.date_order <= '%s'
                        AND po.company_id = %s
                        GROUP BY product_name, pp.id
                        ORDER BY total_qty DESC LIMIT 7
                    """ % (MonthStartDate, MonthEndDate, company_id)
        self._cr.execute(sql_query)
        StockData = self._cr.dictfetchall()

        return StockData