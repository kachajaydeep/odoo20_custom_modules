# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

from odoo import models, _
from odoo.exceptions import UserError

class Irmodel(models.Model):
    _inherit = 'ir.model'


    def copy(self):
        print('\n\n\n >123>>>>', not (self.env.is_admin() or self.env.user.has_group('nf_update_secority.nf_group_no_archive')))
        if self.env.user.has_group('nf_update_secority.nf_group_no_archive'):
            raise UserError(_("You don't have the rights to archive the Records. Please contact an Administrator."))
        return super().copy()