# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super(AccountMove, self).action_post()
        config = self.env['airiv.whatsapp.config'].get_active_config()
        if config.auto_send_invoice:
            self.action_send_whatsapp_invoice_billing()
        return res

    def action_send_whatsapp_invoice_billing(self):
        for move in self:
            if move.move_type not in ('out_invoice', 'out_refund'):
                continue
            partner = move.partner_id
            recipient_phone = partner._get_whatsapp_number()
            if not recipient_phone:
                continue

            template = self.env['airiv.whatsapp.template'].search([('code', '=', 'invoice_post')], limit=1)
            nsfp = getattr(move, 'l10n_id_faktur_pajak_number', '') or 'FAKTUR-STANDAR'
            
            ctx = {
                'partner_name': partner.name,
                'invoice_name': move.name,
                'amount_total': f"Rp {move.amount_total:,.2f}",
                'due_date': move.invoice_date_due.strftime('%d/%m/%Y') if move.invoice_date_due else fields.Date.today().strftime('%d/%m/%Y'),
                'faktur_pajak_number': nsfp,
            }
            body_text = template.render_template(ctx) if template else f"Faktur tagihan {move.name} sebesar Rp {move.amount_total:,.2f} telah diterbitkan."

            msg = self.env['airiv.whatsapp.message'].create({
                'partner_id': partner.id,
                'mobile_raw': recipient_phone,
                'body': body_text,
                'res_model': 'account.move',
                'res_id': move.id,
            })
            msg.action_send()
