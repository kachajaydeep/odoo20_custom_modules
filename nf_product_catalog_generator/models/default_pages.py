# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT. 
# @author:  Part of NextFlowIT. 

from odoo import models, fields, api

class DefaultPages(models.Model):
    _name = 'nf.default.pages'
    _description = 'Default Pages'
    
    # category_name = fields.Char(related='')