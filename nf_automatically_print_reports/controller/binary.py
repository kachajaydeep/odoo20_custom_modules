# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT.

import base64
from odoo import models, api,http
from odoo.http import request

class NfBinary(http.Controller):
    @http.route('/web/nfprintpdf', type="json", auth="user")
    def nf_print_pdf(self, report_name, res_ids=None, data=None):

        if isinstance(res_ids, int):
            res_ids = [res_ids]

        report = request.env['ir.actions.report']

        # 🔥 KEY FIX: handle wizard-based reports
        if data:
            pdf_content, _ = report._render_qweb_pdf(
                report_name,
                res_ids=res_ids,
                data=data
            )
        else:
            pdf_content, _ = report._render_qweb_pdf(
                report_name,
                res_ids=res_ids
            )
            
        return base64.b64encode(pdf_content).decode('utf-8')
