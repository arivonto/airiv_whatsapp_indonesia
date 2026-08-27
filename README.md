# Indonesia WhatsApp Business Messaging Engine (Fonnte & WAHA Sandbox)

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Odoo: 18.0 Community](https://img.shields.io/badge/Odoo-18.0%20Community-purple.svg)](https://www.odoo.com)
[![Price: Free ($0.00)](https://img.shields.io/badge/Price-%240.00%20(Free)-green.svg)](https://airiv.id)
[![Gateway: Fonnte & WAHA](https://img.shields.io/badge/Gateways-Fonnte%20%26%20WAHA-brightgreen.svg)](https://airiv.id)

A native, high-performance WhatsApp Business messaging and notification automation engine built specifically for **Odoo 18.0 Community Edition**. Supports cloud-based **Fonnte REST API** and self-hosted **WAHA (WhatsApp HTTP API)** with an integrated **Offline Sandbox Simulator** for zero-cost pre-testing.

---

## Detailed Capabilities

### 1. Dual Gateway Architecture & Sandbox Simulator
* **Fonnte Cloud REST API**: Direct HTTPS integration (`https://api.fonnte.com/send`) using standard API tokens.
* **WAHA Self-Hosted Engine**: Zero recurring cost Docker container running locally alongside your Odoo stack.
* **Offline Sandbox Simulator**: Safely test triggers, dynamic variable merge compilation, and audit logging with zero API token consumption.

### 2. Indonesian Phone Number Sanitizer
* Automatically converts non-standard phone numbers into international E.164 format:
  * `0812-3456-7890` $\rightarrow$ `6281234567890`
  * `+62 812 3456 7890` $\rightarrow$ `6281234567890`
  * `081234567890` $\rightarrow$ `6281234567890`

### 3. Automated Business Event Triggers
* **Sales Order Confirmation**: Dispatches order summaries with dynamic Midtrans/Xendit instant payment links upon Sales Order confirmation.
* **Logistics & Delivery Dispatch**: Automatically sends courier waybill numbers (*Nomor Resi*) and Biteship public tracking URLs upon Stock Picking validation.
* **Customer Invoicing & Tax Billing**: Delivers invoice notifications with statutory Faktur Pajak NSFP numbers and PDF download links upon posting.

---

## Validated Commercial Workflow (Tested & Scrutinized)

The complete messaging pipeline has been verified under live Odoo 18.0 Community conditions:

1. **Partner Configuration**: Recipient `PT Nusantara Retail Test` configured with WhatsApp number `+62 812-3456-7890`.
2. **Sales Order Alert**: Confirming Sales Order `S00028` triggers automated compilation into clean Indonesian text with payment links, successfully validated via Sandbox logger.
3. **Logistics Dispatch Alert**: Validating outgoing shipment `WH/OUT/00028` interpolates Biteship thermal waybill `Biteship-thermal-resi-jne` and tracking URL into real-time WhatsApp alert.
4. **Audit Trail**: Every outgoing message is preserved in `airiv.whatsapp.message` with full JSON payload and status auditing.

---

## Module Specifications

| Specification | Details |
| :--- | :--- |
| **Framework Version** | Odoo 18.0 Community Edition (OWL client & App Drawer compliant) |
| **License** | GNU Lesser General Public License v3.0 (LGPL-3) |
| **Price** | Free ($0.00) |
| **Dependencies** | `base`, `mail`, `sale`, `account`, `stock` |
| **Server Overhead** | Zero (Native ORM, direct REST stream, no intermediate proxy) |
| **Supported Gateways** | Fonnte REST API, WAHA (Docker), Offline Sandbox |
