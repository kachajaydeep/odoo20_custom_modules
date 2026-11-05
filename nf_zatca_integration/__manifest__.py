# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    'name': 'Zatca Integration Phase 2',
    'version': '20.0.1',
    'depends': ['base', 'base_vat', 'l10n_sa', 'account_edi', 'account_debit_note', 'certificate',
                'account_edi_ubl_cii',],
    'summary': """
        E-Invoicing, Universal Business Language, Zatca, Saudi Arabia, EDI, CII, UBL, Fatoora, Zatka, ZATCA, E-Invoice, 
        EDI Format, Electronic Invoice, Saudi Arabia E-Invoice,
        E-invoice implementation for Saudi Arabia; Integration with ZATCA
        
        Zatka integratoin, Zatca E-invoice, Zatca E-invoicing, Zatca UBL, Zatca CII, Zatca Fatoora,
        Zatca EDI, Zatca Electronic Invoice, Zatca Saudi Arabia E-Invoice
        
        Fatoora integratoin, Fatoora E-invoice, Fatoora E-invoicing, Fatoora UBL, Fatoora CII, Fatoora Zatca,
        Fatoora EDI, Fatoora Electronic Invoice, Fatoora Saudi Arabia E-Invoice
        
        UBL integratoin, UBL E-invoice, UBL E-invoicing, UBL Zatca, UBL CII, UBL Fatoora,
        UBL EDI, UBL Electronic Invoice, UBL Saudi Arabia E-Invoice
        
        Fatoora Portal, EGS (Electronic Generation System), QR codes, unique invoice identifiers, Real-time validation, Digital signatures, Credit/Debit Notes, B2B/B2C invoicing, and Cloud solutions
        
        KSA, KSA ZATCA, KSA Fatoora, KSA UBL, KSA CII, KSA EDI, KSA Electronic Invoice, KSA E-invoice, KSA E-invoicing
        KSA VAT, KSA VAT Compliance, KSA Tax Authority, KSA E-invoicing regulations
        KSA E-invoicing solution, KSA E-invoicing software, KSA E-invoicing system
        KSA E-invoicing integration, KSA E-invoicing module, KSA E-invoicing Odoo
        KSA E-invoicing app, KSA E-invoicing implementation
        KSA E-invoicing automation, KSA E-invoicing management
        KSA E-invoicing reporting, KSA E-invoicing tracking
        KSA E-invoicing compliance, KSA E-invoicing requirements
        KSA E-invoicing standards, KSA E-invoicing guidelines
        KSA E-invoicing best practices, KSA E-invoicing tips
        KSA E-invoicing tricks, KSA E-invoicing hacks
        KSA E-invoicing resources, KSA E-invoicing tools
        KSA E-invoicing services, KSA E-invoicing support
        KSA E-invoicing consulting, KSA E-invoicing training
        KSA E-invoicing certification, KSA E-invoicing accreditation
        KSA E-invoicing partnership, KSA E-invoicing collaboration
        KSA E-invoicing community, KSA E-invoicing forum
        KSA E-invoicing blog, KSA E-invoicing news
        KSA E-invoicing updates, KSA E-invoicing trends
        KSA E-invoicing insights, KSA E-invoicing analysis
        
        KSA Fatoorah, KSA Fatoorah integration, KSA Fatoorah module, KSA Fatoorah app
        KSA Fatoorah implementation, KSA Fatoorah automation, KSA Fatoorah management
        KSA Fatoorah reporting, KSA Fatoorah tracking, KSA Fatoorah compliance
        KSA Fatoorah requirements, KSA Fatoorah standards, KSA Fatoorah guidelines
        KSA Fatoorah best practices, KSA Fatoorah tips, KSA Fatoorah tricks
        KSA Fatoorah hacks, KSA Fatoorah resources
        KSA Fatoorah tools, KSA Fatoorah services, KSA Fatoorah support
        KSA Fatoorah consulting, KSA Fatoorah training, KSA Fatoorah certification
        KSA Fatoorah accreditation, KSA Fatoorah partnership
        KSA Fatoorah collaboration, KSA Fatoorah community
        KSA Fatoorah forum, KSA Fatoorah blog
        
        
        KSA e-invoicing

KSA ZATCA compliance

ZATCA Phase 2

ZATCA Phase 2 integration

Fatoora system KSA

Fatoora compliance Saudi Arabia

Fatoora solution provider

Fatoorah Saudi e-invoice

Fatoorah ZATCA KSA

الفاتورة الإلكترونية السعودية

نظام فاتورة هيئة الزكاة

فاتورة المرحلة الثانية ZATCA

الفاتورة الإلكترونية ZATCA

الفاتوره في السعودية

فاتورة المرحلة الثانية
        
        ZATCA Phase 2 integration in Odoo 18
Odoo Saudi Arabia e-invoicing compliance
ZATCA e-invoicing Odoo 18 module
FATOORAH Odoo integration
Odoo 18 VAT compliance Saudi Arabia
ZATCA Phase 2 electronic invoicing solution
E-invoice integration Odoo KSA

Fatoorah compliance Odoo
Odoo ZATCA certification
ZATCA e-invoice automation Odoo
Odoo ZATCA Phase 2 module
    """,
    'post_init_hook': 'post_init_hook',
    'description': """
ZATCA Phase 2 E-Invoicing Integration in Odoo
===============================================================================
Stay compliant with Saudi Arabia’s ZATCA (Zakat, Tax and Customs Authority) Phase 2 e-invoicing regulations directly inside Odoo 18. Our integration enables businesses to seamlessly generate, validate, and report e-invoices (FATOORAH) in line with the ZATCA e-invoicing Phase 2 requirements, ensuring smooth operations and 100% compliance.

Key Features:

✅ Seamless Integration with Odoo 18 Sales, Invoicing, and Accounting modules
✅ ZATCA-Compliant XML & PDF A/3 Invoices with embedded QR codes
✅ Real-Time Clearance & Reporting through ZATCA APIs (FATOORAH platform)
✅ Cryptographic Stamp & UUID Generation for invoices
✅ Support for Simplified & Standard Tax Invoices
✅ Automatic Validation & Error Handling with ZATCA servers
✅ Customer-Friendly Print Format (Arabic/English) with QR code
✅ Secure Archiving of invoices for audit and compliance
✅ Scalable for Enterprises handling bulk transactions

Why Choose Our ZATCA Phase 2 Integration?
With Saudi Arabia mandating e-invoicing compliance, companies risk penalties without proper implementation. Our ZATCA Odoo 18 integration automates the entire compliance process — from invoice creation to clearance and reporting — saving you time, reducing errors, and ensuring legal compliance with Saudi VAT law.
    """,
    'category': 'Accounting',
    'license': 'LGPL-3',
    'website': 'nextflow.in',
    'author': 'NextFlowIT',
    'data': [
        'security/ir.access.csv',
        'data/zatca_format.xml',
        'data/ubl_21_zatca.xml',
        'data/res_country_data.xml',
        'wizard/nf_zatca_otp_wizard.xml',
        'wizard/nf_account_move_reversal_views.xml',
        'views/nf_account_tax_views.xml',
        'views/nf_account_journal_views.xml',
        'views/nf_res_partner_views.xml',
        'views/nf_res_company_views.xml',
        'views/nf_res_config_settings_view.xml',
        'reports/external_layout_standard_zatca.xml',
        'reports/nf_report_invoice.xml',
        'reports/nf_zatca_report_invoice.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'nf_zatca_integration/static/src/scss/form_view.scss',
        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    "images": ["static/description/background.gif"],
    "price": 250.99,
    "currency": "USD"

}
