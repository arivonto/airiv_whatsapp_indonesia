# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AirivWhatsappTemplate(models.Model):
    _name = 'airiv.whatsapp.template'
    _description = 'AIRIV Indonesian WhatsApp Message Template'

    name = fields.Char(string="Template Name", required=True)
    code = fields.Selection([
        ('sale_order_confirm', 'Sales Order Confirmation & Payment Link'),
        ('stock_dispatch', 'Logistics Dispatch & Waybill (Nomor Resi) Tracking'),
        ('invoice_post', 'Customer Invoice & Faktur Pajak Billing'),
        ('custom', 'Custom Notification'),
    ], string="Template Type", required=True, default='custom')

    body = fields.Text(string="Message Body (Indonesian)", required=True, help="Use dynamic placeholders: {partner_name}, {order_name}, {amount_total}, {resi_number}, {tracking_url}, {invoice_name}")
    active = fields.Boolean(default=True)

    def render_template(self, context_dict):
        self.ensure_one()
        rendered = self.body or ""
        for key, val in context_dict.items():
            rendered = rendered.replace(f"{{{key}}}", str(val or ''))
        return rendered
