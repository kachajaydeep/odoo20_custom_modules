# -*- coding: utf-8 -*-
# Copyright (C) 2021-Today: Part of NextFlowIT.
# @author:  Part of NextFlowIT.

{
    "name": "POS Login with QR Code",
    "summary": """
    POS Login with QR Code for Employees in Odoo pos login with qr code employee qr login for pos cashier login with qr code pos login with qr code employee qr code login for pos cashier login with qr code Employee QR Code Login for POS Cashier Login with QR Code POS Login QR Code Login Odoo POS Security QR Badge Employee POS Access POS QR Authentication Quick POS Login Cashier QR Code Odoo POS QR Module Employee QR Login HR Employee QR Code Badge HR Employee QR Code ID Badge HR Employee QR Code Card HR Employee QR Code Access Card HR Employee QR Code Identification Card HR Employee QR Code Security Badge HR Employee QR Code Verification Badge HR Employee QR Code Authentication Badge HR Employee QR Code Profile Badge HR Employee QR Code Info Badge HR Employee QR Code Details Badge HR Employee QR Code Contact Badge HR Employee QR Code Business Card HR Employee QR Code Identity Badge HR Employee QR Code Work Badge HR Employee QR Code Staff Badge HR Employee QR Code Personnel Badge HR Employee QR Code Member Badge HR Employee QR Code Team Badge HR Employee QR Code Company Badge QR code login for POS cashiers in odoo QR Code authentication for POS cashiers in odoo Quick POS login with QR code for cashiers in odoo Secure POS login with QR code for cashiers in odoo Easy POS login with QR code for cashiers in odoo Fast POS login with QR code for cashiers in odoo Efficient POS login with QR code for cashiers in odoo Reliable POS login with QR code for cashiers in odoo Convenient POS login with QR code for cashiers in odoo Simple POS login with QR code for cashiers in odoo User-friendly POS login with QR code for cashiers in odoo Seamless POS login with QR code for cashiers in odoo Streamlined POS login with QR code for cashiers in odoo Optimized POS login with QR code for cashiers in odoo Enhanced POS login with QR code for cashiers in odoo Improved POS login with QR code for cashiers in odoo Advanced POS login with QR code for cashiers in odoo Innovative POS login with QR code for cashiers in odoo Modern POS login with QR code for cashiers in odoo Cutting-edge POS login with QR code for cashiers in odoo State-of-the-art POS login with QR code for cashiers in odoo Next-generation POS login with QR code for cashiers in odoo Future-proof POS login with QR code for cashiers in odoo restaurant cashier login with qr code restaurant pos login with qr code retail cashier login with qr code retail pos login with qr code store cashier login with qr code store pos login with qr code quick pos login with qr code fast pos login with qr code easy pos login with qr code secure pos login with qr code efficient pos login with qr code reliable pos login with qr code convenient pos login with qr code simple pos login with qr code user-friendly pos login with qr code seamless pos login with qr code streamlined pos login with qr code optimized pos login with qr code enhanced pos login with qr code improved pos login with qr code advanced pos login with qr code innovative pos login with qr code modern pos login with qr code cutting-edge pos login with qr code state-of-the-art pos login with qr code next-generation pos login with qr code future-proof pos login with qr code POS login using qr code Point of Sale Loogin using QR Code Cashier POS login Cashier Point of Sale login cashier pos login cashier login employee login employee pos login employee point of sale login
    """,
    "post_init_hook": "post_init_hook",
    "description": """

POS Login with QR Code
--------------------------------------------
Overview

Simplify your Point of Sale (POS) login process with the POS Login with QR Code module for Odoo.
This app allows employees or cashiers to securely and quickly log in to the POS session by scanning their unique QR code badge - eliminating the need to manually enter PINs every time. Improve efficiency, reduce login errors, and enhance user experience in your retail or restaurant operations.

Key Features
🔐 Generate QR Code from Employee PIN
Automatically generate a unique QR code for each employee based on their POS PIN.

🆔 Employee Identity QR Badge
Each employee can have a personalized QR badge containing their identity and encoded login credentials.

⚡ POS Login via QR Code
Employees can log in to the POS by simply scanning their assigned QR code using a barcode/QR scanner or camera device.

🔄 Seamless Integration with Odoo POS
Works smoothly with Odoo 18 POS module without affecting existing login mechanisms.

👥 Supports Multiple Cashiers
Each cashier has their own secure QR for individual tracking and accountability.

🖨️ Printable QR Badges
Print employee QR badges directly for easy distribution and POS desk display.

Benefits
🚀 Faster Login Process: Save time by avoiding manual PIN entry.
✅ Enhanced Security: Reduces the risk of PIN sharing or misuse.
💼 Professional Identity System: Each employee has a scannable digital badge.
🔄 Fully Compatible: Works out-of-the-box with existing POS configurations.
🧾 Easy Management: Admin can generate, print, or revoke QR codes anytime.
    """,
    "version": "20.0.1",
    "category": "Extra Tools",
    "author": "NextFlowIT",
    "company": "NextFlow Technology",
    "maintainer": "NextFlow Technology",
    "website": "nextflow.in",
    "depends": ["pos_hr"],
    "data": [
        "reports/hr_employee_qr_badge.xml",
        "views/hr_employee_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "nf_pos_login_with_qr/static/src/**/*",
            "https://cdn.rawgit.com/cozmo/jsQR/master/dist/jsQR.js",
        ],
    },
    "external_dependencies": {"python": ["qrcode"]},
    "images": ["static/description/background.gif"],
    "license": "OPL-1",
    "installable": True,
    "auto_install": False,
    "application": False,
    "price": 34.99,
    "currency": "USD",
}
