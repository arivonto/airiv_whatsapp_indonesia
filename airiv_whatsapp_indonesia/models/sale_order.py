# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        config = self.env['airiv.whatsapp.config'].get_active_config()
        if config.auto_send_sale:
            self.action_send_whatsapp_order_confirmation()
        return res

    def action_send_whatsapp_order_confirmation(self):
        for order in self:
            recipient_phone = order.partner_id._get_whatsapp_number()
            if not recipient_phone:
                continue

            template = self.env['airiv.whatsapp.template'].search([('code', '=', 'sale_order_confirm')], limit=1)
            carrier_name = order.carrier_id.name if hasattr(order, 'carrier_id') and order.carrier_id else "Kurir Standar"
            
            ctx = {
                'partner_name': order.partner_id.name,
                'order_name': order.name,
                'amount_total': f"Rp {order.amount_total:,.2f}",
                'carrier_name': carrier_name,
                'payment_url': f"https://airiv.id/pay/{order.name}",
            }
            body_text = template.render_template(ctx) if template else f"Halo {order.partner_id.name}, pesanan {order.name} sebesar Rp {order.amount_total:,.2f} telah dikonfirmasi."

            msg = self.env['airiv.whatsapp.message'].create({
                'partner_id': order.partner_id.id,
                'mobile_raw': recipient_phone,
                'body': body_text,
                'res_model': 'sale.order',
                'res_id': order.id,
            })
            msg.action_send()
