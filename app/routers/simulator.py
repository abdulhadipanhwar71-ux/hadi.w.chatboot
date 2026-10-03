from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from pathlib import Path
from typing import Optional, List
import random
import datetime
import json
import re

from app.database import get_db
from app.models import Message, Customer, Product, Order, OrderItem
from app.services.bot_engine import bot_engine
from app.services.i18n import get_text, get_status_label

router = APIRouter(prefix="/simulator", tags=["WhatsApp Simulator"])

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

class SimulatorMessageRequest(BaseModel):
    phone_number: str = "923001234567"
    message: str

class SimulatorResetRequest(BaseModel):
    phone_number: str = "923001234567"

class SimulatorLanguageRequest(BaseModel):
    phone_number: str = "923001234567"
    language: str = "ur"

class OrderCardSubmitRequest(BaseModel):
    phone_number: str = "923001234567"
    product_code: str
    quantity: int = 1
    customer_name: str
    delivery_address: str
    payment_method: str = "Cash on Delivery"

@router.get("", response_class=HTMLResponse)
async def simulator_page(request: Request, db: Session = Depends(get_db)):
    """Render WhatsApp interactive simulator web UI."""
    return templates.TemplateResponse(request=request, name="simulator.html")

@router.get("/products")
async def get_products_catalog(db: Session = Depends(get_db)):
    """Retrieve available products for simulator interactive address card."""
    products = db.query(Product).filter(Product.is_available == True).order_by(Product.id.asc()).all()
    return {
        "status": "success",
        "products": [
            {
                "id": p.id,
                "code": p.code,
                "name_ur": p.name_ur,
                "name_en": p.name_en,
                "name_sd": p.name_sd,
                "price": p.price
            }
            for p in products
        ]
    }

@router.post("/send")
async def send_simulator_message(data: SimulatorMessageRequest, db: Session = Depends(get_db)):
    """Process incoming test message from simulator and return bot reply."""
    reply = bot_engine.process_incoming_message(db, data.phone_number, data.message)
    return {
        "status": "success",
        "phone_number": data.phone_number,
        "reply": reply
    }

@router.post("/reset")
async def reset_simulator(data: SimulatorResetRequest, db: Session = Depends(get_db)):
    """Reset customer conversation state to clean IDLE and return the main menu."""
    customer = bot_engine.get_or_create_customer(db, data.phone_number)
    customer.conversation_state = "IDLE"
    customer.state_data = "{}"
    db.commit()
    lang = customer.language or "ur"
    reply = get_text("main_menu", lang)
    return {
        "status": "success",
        "phone_number": data.phone_number,
        "language": lang,
        "reply": reply
    }

@router.post("/set_language")
async def set_simulator_language(data: SimulatorLanguageRequest, db: Session = Depends(get_db)):
    """Cleanly switch customer language and immediately return the localized main menu."""
    customer = bot_engine.get_or_create_customer(db, data.phone_number)
    lang = data.language.lower()
    if lang not in ("ur", "en", "sd"):
        lang = "ur"
    customer.language = lang
    customer.conversation_state = "IDLE"
    customer.state_data = "{}"
    db.commit()
    reply = get_text("main_menu", lang)
    return {
        "status": "success",
        "phone_number": data.phone_number,
        "language": lang,
        "reply": reply
    }

@router.get("/orders/{phone_number}")
async def get_customer_orders(phone_number: str, db: Session = Depends(get_db)):
    """Fetch previous and approved orders for a given customer phone number."""
    clean_phone = re.sub(r"[^\d]", "", str(phone_number)).strip()
    orders = db.query(Order).filter(Order.customer_phone == clean_phone).order_by(Order.created_at.desc()).all()
    
    customer = db.query(Customer).filter(Customer.phone_number == clean_phone).first()
    lang = customer.language if customer else "ur"

    orders_list = []
    for o in orders:
        items_summary = [f"{item.product_name} (x{item.quantity})" for item in o.items]
        orders_list.append({
            "id": o.id,
            "order_number": o.order_number,
            "customer_name": o.customer_name,
            "delivery_address": o.delivery_address,
            "total_amount": o.total_amount,
            "payment_method": o.payment_method,
            "status": o.status,
            "status_label": get_status_label(o.status, lang),
            "date": o.created_at.strftime("%Y-%m-%d %I:%M %p"),
            "items": ", ".join(items_summary) if items_summary else "Package"
        })

    return {
        "status": "success",
        "phone_number": clean_phone,
        "count": len(orders_list),
        "orders": orders_list
    }

@router.post("/submit_order_card")
async def submit_order_card(data: OrderCardSubmitRequest, db: Session = Depends(get_db)):
    """Process order submitted directly through the interactive Address & Order Card."""
    clean_phone = re.sub(r"[^\d]", "", str(data.phone_number)).strip() or "923001234567"
    customer = bot_engine.get_or_create_customer(db, clean_phone)
    lang = customer.language or "ur"

    # Find requested product
    product = db.query(Product).filter(
        Product.code == data.product_code.strip().upper(),
        Product.is_available == True
    ).first()

    if not product:
        product = db.query(Product).filter(Product.is_available == True).first()

    if not product:
        raise HTTPException(status_code=400, detail="No active products available in catalog")

    qty = max(1, data.quantity)
    unit_price = float(product.price)
    total_amount = unit_price * qty

    # Update customer record
    customer.name = data.customer_name.strip()
    customer.address = data.delivery_address.strip()
    customer.conversation_state = "IDLE"
    customer.state_data = "{}"

    # Generate unique professional Order ID
    year = datetime.datetime.utcnow().year
    random_num = random.randint(1000, 9999)
    order_number = f"ORD-{year}-{random_num}"

    # Create Order record (Directly Approved/Confirmed from interactive Card)
    order = Order(
        order_number=order_number,
        customer_id=customer.id,
        customer_name=customer.name,
        customer_phone=customer.phone_number,
        delivery_address=customer.address,
        total_amount=total_amount,
        status="CONFIRMED",  # Approved directly via verified order card
        payment_method=data.payment_method
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Create OrderItem
    order_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        product_name=product.get_localized_name(lang),
        unit_price=unit_price,
        quantity=qty,
        subtotal=total_amount
    )
    db.add(order_item)
    db.commit()

    # Log incoming virtual submission
    incoming_summary = (
        f"[📝 ترسیلی پتہ و آرڈر فارم جمع کیا گیا]\n"
        f"پروڈکٹ: {product.get_localized_name(lang)}\n"
        f"تعداد: {qty}\n"
        f"خریدار: {customer.name}\n"
        f"پتہ: {customer.address}\n"
        f"طریقہ ادائیگی: {data.payment_method}"
    )
    bot_engine.log_message(db, customer.phone_number, "INCOMING", incoming_summary, customer.id)

    # Specialized confirmation reply
    if data.payment_method == "EasyPaisa / JazzCash":
        reply = get_text("order_success_jazzcash", lang, order_number=order_number, total=total_amount)
    elif data.payment_method == "Direct Bank Transfer":
        reply = get_text("order_success_bank", lang, order_number=order_number, total=total_amount)
    else:
        reply = get_text("order_success_cod", lang, order_number=order_number, total=total_amount)

    bot_engine.log_message(db, customer.phone_number, "OUTGOING", reply, customer.id)

    return {
        "status": "success",
        "order_number": order_number,
        "customer_name": customer.name,
        "total_amount": total_amount,
        "status_label": get_status_label("CONFIRMED", lang),
        "reply": reply
    }

@router.get("/history/{phone_number}")
async def get_simulator_history(phone_number: str, db: Session = Depends(get_db)):
    """Retrieve chat history for a test phone number."""
    clean_phone = re.sub(r"[^\d]", "", str(phone_number)).strip()
    messages = db.query(Message).filter(Message.phone_number == clean_phone).order_by(Message.timestamp.asc()).all()
    history = [
        {
            "id": m.id,
            "direction": m.direction,
            "content": m.content,
            "timestamp": m.timestamp.strftime("%I:%M %p")
        }
        for m in messages
    ]
    return {"status": "success", "history": history}
