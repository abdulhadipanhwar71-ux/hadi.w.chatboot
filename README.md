# Professional WhatsApp Business Bot (Trilingual: Sindhi, Urdu, English)

A robust, enterprise-grade WhatsApp Business Chatbot and Commerce Engine built with **FastAPI**, **SQLAlchemy**, and **Meta WhatsApp Cloud API**, featuring complete **Pure Sindhi (سنڌي)**, **Urdu (اردو)**, and **English** localization.

---

## 🌟 Key Features (Version 1)

1. **Trilingual Language Selector**:
   - Native support for Pure Sindhi (*سنڌي صورت خطي*), Urdu (*اردو*), and English.
   - Preserves user language preference in the database.
2. **Interactive Main Menu**:
   - Welcome greeting and numeric/keyword menu navigation.
   - Instant return to main menu at any time by typing `0` or `menu`.
3. **Product & Service Catalog**:
   - Localized product names, descriptions, prices (PKR), and stock availability.
4. **Automated Order Placement Flow**:
   - Multi-step conversational state machine (Product selection, quantity validation, customer name, delivery address).
   - Order confirmation summary before placement.
5. **Order Tracking & Status**:
   - Automated unique order tracking code (`ORD-YYYY-XXXX`).
   - Customers can check live status (Pending, Confirmed, Shipped, Delivered, Cancelled) anytime.
6. **Customer Directory & History**:
   - Automatic customer profile creation, address caching, and order association.
7. **Business Info & FAQs**:
   - Automated details on operating hours, nationwide delivery, and payment methods (COD, Bank, JazzCash, EasyPaisa).
8. **Live Human Agent Handoff**:
   - Queues customer support requests directly into the Admin Panel for agent attention.
9. **Interactive WhatsApp Simulator**:
   - Built-in browser-based WhatsApp Web simulator (`/simulator`) to test flows and conversation trees without requiring Meta API credentials upfront.
10. **Modern Web Admin Panel**:
    - **Dashboard**: Business KPIs (Total Revenue, Orders, Pending Orders, Customers, Agent Queue).
    - **Orders Manager**: Search orders, filter by status, and update lifecycle states.
    - **Product Catalog Manager**: Add, edit pricing, toggle availability, and delete products across all 3 languages.
    - **Customer Directory**: View customer records, active states, and order counts.
    - **Message Logs**: Full audit trail of incoming and outgoing communications.

---

## 📁 Project Architecture

```text
D:\whatsapp-business-bot\
├── app\
│   ├── config.py             # Settings and environment variable management
│   ├── database.py           # SQLite / SQLAlchemy connection and session maker
│   ├── models.py             # Database models (Customer, Product, Order, Message, etc.)
│   ├── seed.py               # Initial table setup and sample product seeder
│   ├── services\
│   │   ├── i18n.py           # Sindhi, Urdu, and English localized translation dictionaries
│   │   ├── bot_engine.py     # Conversational state machine and business logic
│   │   └── whatsapp_service.py # Meta WhatsApp Cloud API dispatcher and webhook validator
│   ├── routers\
│   │   ├── webhook.py        # Meta Cloud API Webhook (GET verify, POST incoming)
│   │   ├── simulator.py      # Browser-based test interface routes
│   │   └── admin.py          # Admin Panel endpoints (Orders, Catalog, Customers, KPIs)
│   ├── templates\            # Jinja2 HTML templates for Admin and Simulator
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── orders.html
│   │   ├── products.html
│   │   ├── customers.html
│   │   ├── messages.html
│   │   └── simulator.html
│   └── static\               # CSS and assets
├── data\                     # SQLite database storage (bot_database.db)
├── main.py                   # FastAPI application entry point
├── run.bat                   # Windows batch launcher
├── requirements.txt          # Python dependencies
└── .env                      # Configured environment variables
```

---

## 🚀 Quick Start Guide

### 1. Launch the Server
Double-click `run.bat` or run from PowerShell:
```powershell
cd D:\whatsapp-business-bot
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Access the Interfaces
- **Admin Dashboard**: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
- **Live WhatsApp Simulator**: [http://127.0.0.1:8000/simulator](http://127.0.0.1:8000/simulator)
- **Official Webhook Endpoint**: `http://<your-domain-or-ngrok>/webhook`

---

## 📲 Meta WhatsApp Cloud API Setup (Production)

When ready to connect to a live WhatsApp Business number:
1. Go to the [Meta for Developers Portal](https://developers.facebook.com/).
2. Create or select your Business App and add **WhatsApp**.
3. In **WhatsApp > API Setup**, copy:
   - **Temporary or Permanent Access Token**
   - **Phone Number ID**
4. Paste them into `D:\whatsapp-business-bot\.env`:
   ```ini
   WHATSAPP_TOKEN=your_meta_access_token_here
   WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here
   WHATSAPP_VERIFY_TOKEN=my_secure_webhook_verify_token_123
   ```
5. In **Configuration > Webhook**:
   - Callback URL: `https://<your-domain>/webhook`
   - Verify Token: `my_secure_webhook_verify_token_123`
   - Subscribe to the `messages` event.
