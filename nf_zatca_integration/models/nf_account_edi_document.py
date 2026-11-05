# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models


class AccountEdiDocument(models.Model):
    _inherit = 'account.edi.document'

    def _prepare_jobs(self):
        """
        Override to achieve the following:

        If there is a job to process that may already be part of the chain (posted invoice that timed out),
        Moves it at the beginning of the list.
        """
        jobs = super()._prepare_jobs()
        if len(jobs) > 1:
            move_first_index = 0
            for index, job in enumerate(jobs):
                documents = job['documents']
                if any(d.edi_format_id.code == 'sa_zatca' and d.state == 'to_send' and d.move_id.nf_zatca_chain_index for d in documents):
                    move_first_index = index
                    break
            jobs = [jobs[move_first_index]] + jobs[:move_first_index] + jobs[move_first_index + 1:]

        return jobs
