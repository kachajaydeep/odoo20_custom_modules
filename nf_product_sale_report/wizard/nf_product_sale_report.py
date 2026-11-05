# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import date

class NfProductSaleReport(models.TransientModel):
    _name = 'product.sale.report'
    _description = 'Product Sale Report'
    
    nf_start_date = fields.Date(string="Start Date", required=True)
    nf_end_date = fields.Date(string="End Date", required=True)
    nf_product_category_ids = fields.Many2many('product.category', string="Categories")
    nf_report_type = fields.Selection([('sale', "Sale"),('pos',"Point Of Sale"),('both',"Both")], default="sale", string="Report Type")

    @api.constrains('nf_start_date', 'nf_end_date')
    def _check_date_range(self):
        for rec in self:
            if rec.nf_start_date and rec.nf_end_date:
                if rec.nf_end_date < rec.nf_start_date:
                    raise ValidationError("End Date cannot be earlier than Start Date.")
                if rec.nf_end_date > date.today():
                    raise ValidationError("End Date cannot be in the future.")
            
    def action_btn_create_product_sale_report(self):
        self.ensure_one()

        product_domain = []
        if self.nf_product_category_ids:
            product_domain.append(('categ_id', 'in', self.nf_product_category_ids.ids))
        products = self.env['product.product'].search(product_domain)

        report_lines = {}  # product_id -> {product, qty, on_hand_qty}

        def _accumulate(product, qty, on_hand_qty):
            if product.id not in report_lines:
                report_lines[product.id] = {'product': product, 'qty': 0.0, 'on_hand_qty': 0.0}
            report_lines[product.id]['qty'] += qty
            report_lines[product.id]['on_hand_qty'] = on_hand_qty

        def _get_order_pickings(order):
            """Return outgoing, done pickings for an order.
            Uses picking_ids when sale_stock is installed, otherwise falls
            back to a direct search via the procurement group."""
            if 'picking_ids' in order._fields:
                return order.picking_ids.filtered(
                    lambda p: p.state == 'done' and p.picking_type_code == 'outgoing'
                )
            if 'procurement_group_id' in order._fields and order.procurement_group_id:
                return self.env['stock.picking'].search([
                    ('group_id', '=', order.procurement_group_id.id),
                    ('state', '=', 'done'),
                    ('picking_type_code', '=', 'outgoing'),
                ])
            return self.env['stock.picking']

        if self.nf_report_type in ('sale', 'both'):
            sale_lines = self.env['sale.order.line'].search([
                ('product_id', 'in', products.ids),
                ('order_id.state', '=', 'sale'),
            ])
            for line in sale_lines:
                order = line.order_id
                if order.date_order and self.nf_start_date <= order.date_order.date() <= self.nf_end_date:
                    delivered_qty = 0.0

                    # Only completed delivery orders
                    for picking in _get_order_pickings(order):
                        moves = picking.move_line_ids.filtered(
                            lambda m: m.product_id == line.product_id
                        )
                        for ml in moves:
                            delivered_qty += ml.quantity

                    if delivered_qty > 0:
                        _accumulate(
                            line.product_id,
                            delivered_qty,
                            line.product_id.qty_available
                        )

        if self.nf_report_type in ('pos', 'both'):
            pos_lines = self.env['pos.order.line'].search([
                ('product_id', 'in', products.ids),
                ('order_id.state', 'in', ['paid', 'done']),
            ])
            for line in pos_lines:
                order = line.order_id
                if order.date_order and self.nf_start_date <= order.date_order.date() <= self.nf_end_date:
                    pickings = _get_order_pickings(order)
                    if pickings and not all(p.state == 'done' for p in pickings):
                        continue
                    _accumulate(line.product_id, line.qty, line.product_id.qty_available)

        # Turn dict into a plain list of dicts the template can loop over
        product_line_list = [
            {
                'product_name': v['product'].display_name,
                'qty': v['qty'],
                'on_hand_qty': v['on_hand_qty'],
            }
            for v in report_lines.values()
        ]

        # Convert category recordset -> comma separated names
        categories = ', '.join(self.nf_product_category_ids.mapped('name')) or 'All'

        # Convert selection key -> human readable label
        report_type_label = dict(
            self._fields['nf_report_type'].selection
        ).get(self.nf_report_type)

        total_product_count = len(product_line_list)
        total_qty = sum(v['qty'] for v in report_lines.values())

        return self.env.ref('nf_product_sale_report.action_report_product').report_action(
            self,
            data={
                'product_line_list': product_line_list,
                'start_date': self.nf_start_date,
                'end_date': self.nf_end_date,
                'categories': categories,
                'report_type': report_type_label,
                'total_product_count': total_product_count,
                'total_qty': total_qty,
            }
        )