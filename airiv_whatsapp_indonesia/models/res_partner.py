# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_id_whatsapp = fields.Char(string="WhatsApp Number (+62)", help="Indonesian mobile phone number for WhatsApp alerts")

    def _get_whatsapp_number(self):
        self.ensure_one()
        return self.l10n_id_whatsapp or self.mobile or self.phone or ""
