# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author: Part of NextFlowIT.

import re
import base64
import openpyxl
from io import BytesIO
import logging

from odoo import _, api, fields, models #type: ignore
from odoo.exceptions import UserError, ValidationError  #type: ignore

_logger = logging.getLogger(__name__)

class PosImportWizard(models.TransientModel):
    _name = 'nf.pos.import.wizard'
    _description = 'POS Order Import Wizard'
    
    session_id = fields.Many2one('pos.session', string='Fallback Session', required=True)
    payment_method_id = fields.Many2one('pos.payment.method', string='Fallback Payment Method', required=True)
    file = fields.Binary(string='XLSX File', required=True)
    filename = fields.Char()
    import_result = fields.Text(string='Result', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], default='draft')

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    @api.constrains('file', 'filename')
    def _check_excel_file(self):
        for wizard in self:
            if not wizard.file:
                continue

            if not wizard.filename:
                raise ValidationError(_("Please upload an Excel file."))

            if not wizard.filename.lower().endswith('.xlsx'):
                raise ValidationError(_("Only .xlsx Excel files are supported."))

    # -------------------------------------------------------------------------
    # Main Import
    # -------------------------------------------------------------------------

    def action_import(self):
        self.ensure_one()

        if not self.file:
            raise UserError(_("Please upload an Excel file."))

        worksheet = self._get_worksheet()
        columns = self._get_columns(worksheet)

        has_order_lines = 'Order Lines' in columns

        self._validate_columns(columns, has_order_lines)

        # Caches to avoid repeated database searches.
        cache = {'sessions': {}, 'configs': {}, 'partners': {}, 'employees': {}, 'products': {}}

        session_sequences = {}
        errors = []
        orders_created = 0

        current_order = self.env['pos.order']
        current_status = 'draft'

        for row_number, row in enumerate(
            worksheet.iter_rows(min_row=2, values_only=True),   #type: ignore
            start=2,
        ):
            if not any(row):
                continue

            try:
                order_ref = self._get_value(row, columns, 'Order Ref')

                if order_ref:
                    # Finalize previous order before starting a new one.
                    if current_order:
                        self._finalize_order(current_order, current_status, has_order_lines)

                    current_order = self.env['pos.order']

                    order_data = self._prepare_order(
                        row=row,
                        columns=columns,
                        cache=cache,
                        session_sequences=session_sequences,
                    )

                    order_ref = order_data['name']

                    if self._order_exists(order_ref):
                        errors.append(
                            _(
                                'Row %(row)s: Order Ref "%(ref)s" '
                                'already exists.',
                                row=row_number,
                                ref=order_ref,
                            )
                        )
                        continue

                    current_order = self.env['pos.order'].create(order_data)

                    orders_created += 1
                    current_status = self._get_order_status(row, columns)

                # Add line to current order.
                if has_order_lines and current_order:
                    self._create_line_from_row(
                        order=current_order,
                        row=row,
                        columns=columns,
                        cache=cache,
                        row_number=row_number,
                        errors=errors,
                    )

            except Exception as error:
                errors.append(
                    _('Row %(row)s: %(error)s', row=row_number, error=str(error))
                )

                # Do not carry a partially processed order into the next row.
                current_order = self.env['pos.order']
                current_status = 'draft'

                # Detailed traceback is useful in server logs,
                # but normally should not be shown to the user.
                _logger.warn("POS Excel import failed at row %s", row_number)

        # Finalize last order.
        if current_order:
            self._finalize_order(current_order, current_status, has_order_lines)

        result = self._build_import_result(
            orders_created=orders_created,
            has_order_lines=has_order_lines,
            errors=errors,
        )

        self.write({
            'import_result': result,
            'state': 'done',
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    # -------------------------------------------------------------------------
    # Excel Helpers
    # -------------------------------------------------------------------------

    def _get_worksheet(self):
        try:
            file_value = self.file

            # BinaryValueAttachment.content contains the actual binary content.
            file_data = file_value.content

            if not file_data:
                raise UserError(_("The uploaded file is empty."))

            workbook = openpyxl.load_workbook(
                filename=BytesIO(file_data),
                read_only=True,
                data_only=True,
            )

            return workbook.active

        except Exception as error:
            raise UserError(
                _(
                    "The uploaded file could not be read as an Excel "
                    "(.xlsx) file.\n\nError: %s"
                ) % error
            )

    @staticmethod
    def _get_columns(worksheet):
        headers = [
            str(cell.value).strip()
            if cell.value is not None
            else ''
            for cell in worksheet[1]
        ]

        return { header: index for index, header in enumerate(headers) if header }

    def _validate_columns(self, columns, has_order_lines):
        required_columns = {'Order Ref', 'Session',}

        if has_order_lines:
            required_columns.update({'Order Lines', 'Quantity', 'Unit Price'})

        missing_columns = sorted(
            required_columns - columns.keys()
        )

        if missing_columns:
            raise UserError(
                _(
                    "The uploaded file is missing required column(s): %s"
                ) % ', '.join(missing_columns)
            )

    @staticmethod
    def _get_value(row, columns, column_name):
        index = columns.get(column_name)

        if index is None:
            return False

        return row[index]

    # -------------------------------------------------------------------------
    # Order Preparation
    # -------------------------------------------------------------------------

    def _prepare_order(self, row, columns, cache, session_sequences):
        order_ref = self._get_value(row, columns, 'Order Ref')

        if not order_ref:
            raise UserError(_("Order Ref is missing."))

        session = self._find_session(self._get_value(row, columns, 'Session'), cache)
        sequence_number = self._get_next_sequence_number(session, session_sequences)
        pos_reference = self._get_receipt_number(row, columns)
        config = self._find_config(self._get_value(row, columns, 'Point of Sale'), session, cache)
        partner = self._find_partner(self._get_value(row, columns, 'Customer'), cache)
        employee = self._find_employee(self._get_value(row, columns, 'Employee'), cache)
        date_order = self._get_value(row, columns, 'Date')

        return {
            'name': str(order_ref).strip(),
            'session_id': session.id,
            'config_id': config.id,
            'partner_id': partner.id if partner else False,
            'employee_id': employee.id if employee else False,
            'pos_reference': pos_reference,
            'date_order': date_order or fields.Datetime.now(),
            'state': 'draft',
            'amount_tax': 0.0,
            'amount_total': 0.0,
            'amount_paid': 0.0,
            'amount_return': 0.0,
            'pricelist_id': (
                config.pricelist_id.id
                if config.pricelist_id
                else False
            ),
            'currency_id': session.currency_id.id,
            'sequence_number': sequence_number,
        }

    def _get_order_status(self, row, columns):
        status = self._get_value(row, columns, 'Status')
        status = str(status or '').strip().lower()

        return {'paid': 'paid', 'posted': 'done'}.get(status, 'draft')

    # -------------------------------------------------------------------------
    # Session / Config / Partner / Employee
    # -------------------------------------------------------------------------

    def _find_session(self, session_name, cache):
        if session_name:
            session_name = str(session_name).strip()

            if session_name in cache['sessions']:
                return cache['sessions'][session_name]

            session = self.env['pos.session'].search(
                [('name', '=', session_name)],
                limit=1,
            )

            if session:
                cache['sessions'][session_name] = session
                return session

        return self.session_id

    def _find_config(self, config_name, session, cache):
        if config_name:
            config_name = str(config_name).strip()

            if config_name in cache['configs']:
                return cache['configs'][config_name]

            config = self.env['pos.config'].search(
                [('name', '=', config_name)],
                limit=1,
            )

            if config:
                cache['configs'][config_name] = config
                return config

        return session.config_id

    def _find_partner(self, partner_name, cache):
        if not partner_name:
            return self.env['res.partner']

        partner_name = str(partner_name).strip()

        if partner_name in cache['partners']:
            return cache['partners'][partner_name]

        partner = self.env['res.partner'].search(
            [('name', '=', partner_name)],
            limit=1,
        )

        cache['partners'][partner_name] = partner

        return partner

    def _find_employee(self, employee_name, cache):
        if not employee_name:
            return self.env['hr.employee']

        employee_name = str(employee_name).strip()

        if employee_name in cache['employees']:
            return cache['employees'][employee_name]

        employee = self.env['hr.employee'].search(
            [('name', '=', employee_name)],
            limit=1,
        )

        cache['employees'][employee_name] = employee

        return employee

    # -------------------------------------------------------------------------
    # Sequence / Receipt Number
    # -------------------------------------------------------------------------

    def _get_next_sequence_number(self, session, session_sequences):
        if session.id not in session_sequences:
            last_order = self.env['pos.order'].search(
                [('session_id', '=', session.id)],
                order='sequence_number desc',
                limit=1,
            )

            session_sequences[session.id] = (
                last_order.sequence_number or 0
            )

        session_sequences[session.id] += 1

        return session_sequences[session.id]

    def _get_receipt_number(self, row, columns):
        receipt_number = self._get_value(row, columns, 'Receipt Number')

        if not receipt_number:
            raise UserError(
                _("Receipt Number is missing. " "Please add it to the file.")
            )

        receipt_number = str(receipt_number).strip()

        # Example: 1-2-000001
        if not re.fullmatch(r'\d+-\d+-\d{6}', receipt_number):
            raise UserError(
                _(
                    'Receipt Number "%s" has an invalid format. '
                    'Expected format: "1-2-000001".'
                ) % receipt_number
            )

        existing_order = self.env['pos.order'].search(
            [('pos_reference', '=', receipt_number)],
            limit=1,
        )

        if existing_order:
            raise UserError(
                _(
                    'Receipt Number "%s" already exists '
                    '(Order: %s).'
                ) % (
                    receipt_number,
                    existing_order.name,
                )
            )

        return receipt_number

    def _order_exists(self, order_ref):
        return bool(
            self.env['pos.order'].search(
                [('name', '=', order_ref)],
                limit=1,
            )
        )

    # -------------------------------------------------------------------------
    # Order Lines
    # -------------------------------------------------------------------------

    def _create_line_from_row(self, order, row, columns, cache, row_number, errors):
        product_value = self._get_value(row, columns, 'Order Lines')

        if not product_value:
            return

        match = re.match(r'\[(.+?)\]\s*(.+)', str(product_value).strip(),)

        if not match:
            errors.append(
                _(
                    'Row %(row)s: Invalid product format "%(product)s". '
                    'Expected "[Internal Reference] Product Name".'
                ) % {
                    'row': row_number,
                    'product': product_value,
                }
            )
            return

        internal_ref = match.group(1).strip()
        product_name = match.group(2).strip()

        product = self._find_product(internal_ref, product_name, cache)

        if not product:
            errors.append(
                _(
                    'Row %(row)s: Product "%(product)s" '
                    'could not be found.'
                ) % {
                    'row': row_number,
                    'product': product_value,
                }
            )
            return

        quantity = self._get_float_value(row, columns, 'Quantity', default=1.0)

        price_unit = self._get_float_value(row, columns, 'Unit Price', default=0.0)

        self.env['pos.order.line'].create({
            'order_id': order.id,
            'product_id': product.id,
            'qty': quantity,
            'price_unit': price_unit,
            'price_subtotal': quantity * price_unit,
            'price_subtotal_incl': quantity * price_unit,
        })

    def _find_product(self, internal_ref, product_name, cache):
        cache_key = (internal_ref, product_name)

        if cache_key in cache['products']:
            return cache['products'][cache_key]

        product = self.env['product.product'].search(
            [('default_code', '=', internal_ref)],
            limit=1,
        )

        if not product:
            product = self.env['product.product'].search(
                [('name', '=', product_name)],
                limit=1,
            )

        cache['products'][cache_key] = product

        return product

    # -------------------------------------------------------------------------
    # Finalization
    # -------------------------------------------------------------------------

    def _finalize_order(self, order, order_status, has_order_lines):
        if not order:
            return

        if has_order_lines:
            self._recompute_order_amounts(order)

            if order_status in ('paid', 'done'):
                self._create_payment(order, order_status)
                
        else:
            order.write({ 'state': 'draft' })

    def _recompute_order_amounts(self, order):
        amount_total = sum(
            order.lines.mapped('price_subtotal_incl')
        )

        amount_subtotal = sum(
            order.lines.mapped('price_subtotal')
        )

        order.write({
            'amount_tax': amount_total - amount_subtotal,
            'amount_total': amount_total,
        })

    def _create_payment(self, order, order_status):
        if not self.payment_method_id:
            return

        self.env['pos.payment'].create({
            'pos_order_id': order.id,
            'amount': order.amount_total,
            'payment_method_id': self.payment_method_id.id,
            'session_id': order.session_id.id,
        })

        order.write({
            'state': order_status,
            'amount_paid': order.amount_total,
        })

    # -------------------------------------------------------------------------
    # Utility
    # -------------------------------------------------------------------------

    @staticmethod
    def _get_float_value(row, columns, column_name, default=0.0):
        value = row[columns[column_name]]

        if value in (None, ''):
            return default

        try:
            return float(value)
        except (TypeError, ValueError):
            raise UserError(_('Column "%s" must contain a number.') % column_name)

    @staticmethod
    def _build_import_result(orders_created, has_order_lines, errors):
        result = _('Successfully imported %s orders.') % orders_created

        if not has_order_lines:
            result += _(
                '\n\nWarning: No order lines were imported. '
                'Add lines manually from POS.'
            )

        if errors:
            result += _('\n\nErrors (%s):\n%s') % (
                len(errors),
                '\n'.join(errors),
            )

        return result