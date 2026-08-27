# -*- coding: utf-8 -*-
import json
import re
import urllib.request
import urllib.error
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AirivWhatsappMessage(models.Model):
    _name = 'airiv.whatsapp.message'
    _description = 'AIRIV WhatsApp Message Audit Log'
    _order = 'create_date desc'

    name = fields.Char(string="Message Reference", required=True, copy=False, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string="Recipient Partner")
    mobile_raw = fields.Char(string="Original Phone Number")
    mobile_sanitized = fields.Char(string="Sanitized Target (628xx)", compute="_compute_sanitized_number", store=True)
    body = fields.Text(string="Message Payload Text", required=True)
    attachment_url = fields.Char(string="Attachment / Tracking URL")
    filename = fields.Char(string="Attachment Filename")
    
    provider = fields.Selection([
        ('fonnte', 'Fonnte Cloud REST API'),
        ('waha', 'WAHA Docker Engine'),
    ], string="Gateway", default='fonnte')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('simulated', 'Simulated (Sandbox Mode)'),
        ('sent', 'Sent to WhatsApp Gateway'),
        ('failed', 'Delivery Failed'),
    ], string="Status", default='draft', tracking=True)

    response_payload = fields.Text(string="Gateway Raw Response", readonly=True)
    error_message = fields.Char(string="Error Details", readonly=True)

    res_model = fields.Char(string="Related Document Model")
    res_id = fields.Integer(string="Related Document ID")

    @api.depends('mobile_raw')
    def _compute_sanitized_number(self):
        for rec in self:
            rec.mobile_sanitized = self._sanitize_phone(rec.mobile_raw)

    @api.model
    def _sanitize_phone(self, phone_input):
        if not phone_input:
            return ""
        cleaned = re.sub(r'\D', '', str(phone_input))
        if cleaned.startswith('08'):
            cleaned = '628' + cleaned[2:]
        elif cleaned.startswith('8'):
            cleaned = '628' + cleaned[1:]
        elif cleaned.startswith('6208'):
            cleaned = '628' + cleaned[4:]
        return cleaned

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('airiv.whatsapp.message') or f"WA-{fields.Date.today().strftime('%Y%m%d')}-{fields.Datetime.now().strftime('%H%M%S')}"
        return super().create(vals_list)

    def action_send(self):
        config = self.env['airiv.whatsapp.config'].get_active_config()
        for msg in self:
            target = msg.mobile_sanitized
            if not target or len(target) < 10 or not target.startswith("628"):
                msg.write({
                    'state': 'failed',
                    'error_message': f"Invalid Indonesian phone number: {msg.mobile_raw} -> {target}"
                })
                continue

            # 1. Sandbox Offline Mode
            if config.environment == 'sandbox' or not config.fonnte_api_token or 'MOCK' in (config.fonnte_api_token or ''):
                mock_response = {
                    "status": True,
                    "id": f"fonnte_mock_{target[-4:]}_{fields.Date.today().strftime('%Y%m%d')}",
                    "target": [target],
                    "process": "simulated_success",
                    "mode": "SANDBOX_SIMULATION"
                }
                msg.write({
                    'state': 'simulated',
                    'response_payload': json.dumps(mock_response, indent=2),
                    'error_message': False,
                })
                continue

            # 2. Live Fonnte REST API
            if config.provider == 'fonnte':
                payload = {
                    "target": target,
                    "message": msg.body,
                    "countryCode": "62"
                }
                if msg.attachment_url:
                    payload["url"] = msg.attachment_url
                if msg.filename:
                    payload["filename"] = msg.filename

                headers = {
                    "Authorization": config.fonnte_api_token,
                    "Content-Type": "application/json"
                }
                req = urllib.request.Request(config.fonnte_endpoint, data=json.dumps(payload).encode('utf-8'), headers=headers)
                try:
                    with urllib.request.urlopen(req, timeout=12) as resp:
                        resp_data = json.loads(resp.read().decode('utf-8'))
                        msg.write({
                            'state': 'sent' if resp_data.get('status') else 'failed',
                            'response_payload': json.dumps(resp_data, indent=2),
                            'error_message': resp_data.get('reason') or False
                        })
                except Exception as e:
                    msg.write({
                        'state': 'failed',
                        'error_message': str(e)
                    })
