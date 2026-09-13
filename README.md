# Indonesia WhatsApp Business Messaging Engine

[![Odoo](https://img.shields.io/badge/Odoo-18.0-714B67.svg)](https://www.odoo.com/)
[![License](https://img.shields.io/badge/License-LGPL--3-0f766e.svg)](LICENSE)
[![Author](https://img.shields.io/badge/Author-AIRIV-0891b2.svg)](https://airiv.id)
[![GitHub Actions](https://github.com/arivonto/airiv_whatsapp_indonesia/actions/workflows/odoo-appstore-ci.yml/badge.svg?branch=18.0)](https://github.com/arivonto/airiv_whatsapp_indonesia/actions)
[![Apps Store Ready](https://img.shields.io/badge/Odoo%20Apps%20Store-ready-22c55e.svg)](https://apps.odoo.com/)

`airiv_whatsapp_indonesia` is an Indonesian WhatsApp Business automation engine for Odoo 18 Community. It connects sales, delivery, invoicing, partners, and audit logs into one controlled messaging rail with Fonnte, WAHA, and an offline sandbox mode.

The module is designed for practical Indonesian operating flows: sales order confirmation, payment reminder context, delivery waybill notification, Biteship/RajaOngkir-style tracking links, invoice billing alerts, Faktur Pajak reference messaging, and clean phone normalization for local numbers.

## Core Capabilities

- Dual gateway rail for Fonnte Cloud REST API and WAHA self-hosted WhatsApp HTTP API.
- Offline sandbox simulator for safe demos, QA, and template testing without consuming gateway tokens.
- Indonesian phone sanitizer that normalizes `08xx`, `8xx`, `+62`, and punctuation-heavy phone numbers into gateway-ready `628xx` format.
- Automated sales order confirmation messages with customer name, order number, total amount, carrier context, and payment link placeholders.
- Automated outgoing delivery alerts from stock picking validation with waybill number and tracking URL context.
- Automated customer invoice alerts from posted invoices with amount, due date, invoice number, and Faktur Pajak reference placeholders.
- Localized template library using simple merge variables such as `{partner_name}`, `{order_name}`, `{invoice_name}`, `{resi_number}`, and `{tracking_url}`.
- Full message audit trail in Odoo with partner, source document, sanitized phone number, state, response payload, and error message.
- AIRIV OS-ready positioning so the module can appear as part of a wider AIRIV vertical ERP portfolio.

## Architecture

```text
Odoo Business Event
  |
  |-- sale.order action_confirm
  |-- stock.picking button_validate
  |-- account.move action_post
  v
AIRIV WhatsApp Automation Layer
  |
  |-- airiv.whatsapp.template
  |-- airiv.whatsapp.config
  |-- airiv.whatsapp.message
  v
Gateway Decision
  |
  |-- Sandbox Simulator
  |-- Fonnte REST API
  |-- WAHA HTTP API
  v
Customer WhatsApp Message + Odoo Audit Log
```

The module stays native to Odoo. It does not require an external middleware server for the core automation flow. Production delivery can use Fonnte or WAHA, while the sandbox path keeps demonstrations and internal validation safe.

## Feature & Workflow Automation

### 1. Sales Order Confirmation

When a sales order is confirmed, the module can compile and send an Indonesian WhatsApp message with:

- customer name,
- sales order number,
- order total,
- carrier context,
- payment link placeholder,
- source document reference.

This helps sales teams turn an Odoo confirmation into a customer-facing notification without leaving the ERP.

### 2. Logistics Dispatch Alert

When an outgoing delivery is validated, the module can send:

- courier/carrier name,
- waybill number,
- Biteship/RajaOngkir-style tracking URL,
- delivery reference,
- customer identity.

The result is a cleaner handoff between warehouse operations and customer communication.

### 3. Invoice and Tax Billing Alert

When a customer invoice is posted, the module can send:

- invoice number,
- invoice amount,
- due date,
- tax reference context,
- PDF or external attachment URL placeholder.

This makes billing follow-up feel integrated instead of manually copied from accounting screens.

### 4. Sandbox QA Loop

Sandbox mode lets teams test templates, placeholders, recipient resolution, and audit records without sending real WhatsApp messages. This is useful for:

- implementation QA,
- app store demonstrations,
- training sessions,
- customer proof-of-concept environments,
- troubleshooting gateway credentials.

## Technical Specifications

| Area | Specification |
| --- | --- |
| Odoo version | 18.0 Community |
| Module name | `airiv_whatsapp_indonesia` |
| License | LGPL-3 |
| Author | AIRIV |
| Website | https://airiv.id |
| Repository | https://github.com/arivonto/airiv_whatsapp_indonesia |
| Main models | `airiv.whatsapp.config`, `airiv.whatsapp.template`, `airiv.whatsapp.message` |
| Business integrations | `sale.order`, `stock.picking`, `account.move`, `res.partner` |
| Gateways | Fonnte REST API, WAHA HTTP API, Sandbox |
| Default Fonnte endpoint | `https://api.fonnte.com/send` |
| Default WAHA endpoint | `http://localhost:3000/api/sendText` |
| Required dependencies | `base`, `mail`, `sale`, `account`, `stock`, `airiv_os_core` |
| Store assets | `static/description/icon.png`, `static/description/banner.png`, `static/description/index.html` |

## Installation Guidance

1. Clone the repository on branch `18.0`.

```bash
git clone --branch 18.0 git@github.com:arivonto/airiv_whatsapp_indonesia.git
```

2. Add the module folder to your Odoo addons path.

```text
airiv_whatsapp_indonesia/airiv_whatsapp_indonesia
```

3. Restart Odoo and update the apps list.

4. Install **Indonesia WhatsApp Business Messaging Engine (Fonnte & WAHA Sandbox)** from Apps.

5. Open the WhatsApp Center menu and configure the active gateway:

- use sandbox mode for safe testing,
- use Fonnte for cloud delivery,
- use WAHA for self-hosted delivery.

6. Review templates before enabling automated sending for sales, delivery, or invoice workflows.

## Configuration Checklist

- Configure partner WhatsApp numbers in Indonesian local or international format.
- Create or activate one `airiv.whatsapp.config` record.
- Start with sandbox mode and confirm that message logs are generated correctly.
- Review default templates and adapt the wording to your company tone.
- Enable automation flags gradually: Sales, Delivery, then Invoice.
- Move to production gateway credentials only after sandbox results are correct.

## Repository Layout

```text
airiv_whatsapp_indonesia/
  __manifest__.py
  data/
    whatsapp_template_data.xml
  models/
    whatsapp_config.py
    whatsapp_message.py
    whatsapp_template.py
    sale_order.py
    stock_picking.py
    account_move.py
    res_partner.py
  security/
    ir.model.access.csv
  static/description/
    icon.png
    banner.png
    index.html
  views/
    whatsapp_config_views.xml
    whatsapp_template_views.xml
    whatsapp_message_views.xml
    whatsapp_menu_views.xml
```

## Author & Contact

| Field | Details |
| --- | --- |
| Author | AIRIV |
| Website | https://airiv.id |
| GitHub | https://github.com/arivonto |
| Module repository | https://github.com/arivonto/airiv_whatsapp_indonesia |
| Odoo series | 18.0 |

## Quality Gate

This repository includes an Odoo Apps Store CI audit through GitHub Actions. The audit checks manifest metadata, required store assets, import safety, README presence, and Apps Store packaging readiness on branch `18.0`.
