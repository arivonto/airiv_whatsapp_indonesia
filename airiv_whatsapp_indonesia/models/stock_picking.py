# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        config = self.env['airiv.whatsapp.config'].get_active_config()
        if config.auto_send_picking:
            self.action_send_whatsapp_dispatch_alert()
        return res

    def action_send_whatsapp_dispatch_alert(self):
        for picking in self:
            if picking.picking_type_code != 'outgoing':
                continue
            partner = picking.partner_id
            if not partner:
                continue
            recipient_phone = partner._get_whatsapp_number()
            if not recipient_phone:
                continue

            template = self.env['airiv.whatsapp.template'].search([('code', '=', 'stock_dispatch')], limit=1)
            resi = getattr(picking, 'carrier_tracking_ref', False) or getattr(picking, 'airiv_waybill_number', False) or 'SEDANG_PROSES'
            carrier_name = picking.carrier_id.name if picking.carrier_id else "Ekspedisi Indonesia"
            tracking_url = picking.carrier_id.get_tracking_link(picking) if picking.carrier_id and hasattr(picking.carrier_id, 'get_tracking_link') else f"https://track.biteship.com/{resi}"

            ctx = {
                'partner_name': partner.name,
                'order_name': picking.origin or picking.name,
                'carrier_name': carrier_name,
                'resi_number': resi,
                'tracking_url': tracking_url,
            }
            body_text = template.render_template(ctx) if template else f"Pesanan {picking.origin or picking.name} telah dikirim dengan nomor resi {resi}."

            msg = self.env['airiv.whatsapp.message'].create({
                'partner_id': partner.id,
                'mobile_raw': recipient_phone,
                'body': body_text,
                'attachment_url': tracking_url,
                'res_model': 'stock.picking',
                'res_id': picking.id,
            })
            msg.action_send()
