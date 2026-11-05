# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

from odoo import models, api

class NfProductReportAbstractModel(models.AbstractModel):
    _name = "report.nf_product_sale_report.product_sale_report"
    _description = "Product Sale Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['product.sale.report'].browse(docids)
        return {
            "doc_ids": docids,
            "doc_model": "product.sale.report",
            "docs": docs,
            "product_line_list": data.get('product_line_list') if data else [],
            "start_date": data.get('start_date') if data else '',
            "end_date": data.get('end_date') if data else '',
            'categories' : data.get('categories') if data else '',
            'report_type' : data.get('report_type') if data else '',
            "total_product_count": data.get('total_product_count') if data else 0,
            "total_qty": data.get('total_qty') if data else 0.0,
        }