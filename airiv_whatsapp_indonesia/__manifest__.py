# -*- coding: utf-8 -*-
{
    'name': 'Indonesia WhatsApp Business Messaging Engine (Fonnte & WAHA Sandbox)',
    'version': '18.0.1.0.0',
    'category': 'Extra Tools/Discuss',
    'summary': 'Automated WhatsApp Notifications for Orders, Invoices, Biteship Resi, and Payslips with Fonnte & Sandbox',
    'description': """
Indonesia WhatsApp Business Automation & Messaging Engine for Odoo 18 Community.
- Dual Gateway Rails: Fonnte Cloud REST API & WAHA (WhatsApp HTTP API Docker)
- Native Offline Sandbox Simulator: Test messaging payloads with zero API token consumption
- Indonesian Phone Sanitizer: Automatically formats local numbers (+62 / 08xx -> 628xx)
- Automated Event Triggers:
  * Sales Order Confirm: Send order summary & Midtrans/Xendit payment links
  * Logistics Dispatch: Send courier name, Biteship/RajaOngkir nomor resi & tracking URL
  * Invoicing: Send invoice summary, Faktur Pajak NSFP, and PDF attachment links
- Localized Indonesian Template Library with dynamic merge variables
- Zero External Server Overhead - 100% Odoo 18 Community Native
""",
    'author': 'Riv Cloud Management',
    'website': 'https://airiv.id',
    'license': 'LGPL-3',
    'price': 0.0,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'sale', 'account', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/whatsapp_template_data.xml',
        'views/whatsapp_config_views.xml',
        'views/whatsapp_template_views.xml',
        'views/whatsapp_message_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/account_move_views.xml',
        'views/whatsapp_menu_views.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
