# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 


from odoo import models, fields 

class ResPartner(models.Model):
    _inherit='res.partner'

    # create fields
    license_no = fields.Char(string="License No")
    id_proof_attachment = fields.Binary(string="ID Proof Attachment")
    id_proof_name = fields.Char(string="ID Proof Name")
    birth_date = fields.Date(string="Birth Date")