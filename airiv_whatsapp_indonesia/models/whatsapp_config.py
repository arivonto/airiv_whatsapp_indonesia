# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.error
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AirivWhatsappConfig(models.Model):
    _name = 'airiv.whatsapp.config'
    _description = 'AIRIV WhatsApp Gateway Configuration'

    name = fields.Char(string="Configuration Name", required=True, default="AIRIV WhatsApp Gateway")
    provider = fields.Selection([
        ('fonnte', 'Fonnte Cloud REST API (api.fonnte.com)'),
        ('waha', 'WAHA - WhatsApp HTTP API (Self-Hosted Docker)'),
    ], string="Gateway Provider", default='fonnte', required=True)

    environment = fields.Selection([
        ('sandbox', 'Sandbox (Offline Simulation - Zero Cost)'),
        ('production', 'Live Production Gateway'),
    ], string="Environment Mode", default='sandbox', required=True)

    fonnte_api_token = fields.Char(string="Fonnte API Token", help="API token obtained from Fonnte dashboard")
    fonnte_endpoint = fields.Char(string="Fonnte REST Endpoint", default="https://api.fonnte.com/send", required=True)

    waha_endpoint = fields.Char(string="WAHA REST Endpoint", default="http://localhost:3000/api/sendText", help="Endpoint for local/Docker WAHA instance")
    waha_session = fields.Char(string="WAHA Session Name", default="default")
    waha_api_key = fields.Char(string="WAHA API Key")

    auto_send_sale = fields.Boolean(string="Auto-send on Sales Order Confirmation", default=True)
    auto_send_picking = fields.Boolean(string="Auto-send on Shipping Dispatch", default=True)
    auto_send_invoice = fields.Boolean(string="Auto-send on Invoice Validation", default=True)
    active = fields.Boolean(default=True)

    @api.model
    def get_active_config(self):
        config = self.search([('active', '=', True)], limit=1)
        if not config:
            config = self.create({
                'name': 'AIRIV Default WhatsApp Config',
                'provider': 'fonnte',
                'environment': 'sandbox',
            })
        return config
