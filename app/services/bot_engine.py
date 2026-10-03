"""
Core conversational engine managing state machine, multilingual flows, and real-world commerce lifecycle.
All code and comments are strictly in standard English.
"""

import json
import random
import datetime
import re
from typing import Tuple, List, Optional
from sqlalchemy.orm import Session

from app.models import Customer, Product, Order, OrderItem, Message, AgentHandoff
from app.services.i18n import get_text, get_status_label

class BotEngine:
    """Enterprise conversational engine for WhatsApp Business automation."""

    def get_or_create_customer(self, db: Session, phone_number: str) -> Customer:
        """Find existing customer or create a new customer record."""
        clean_phone = re.sub(r"[^\d]", "", str(phone_number or "923001234567")).strip()
        if not clean_phone:
            clean_phone = "923001234567"

        customer = db.query(Customer).filter(Customer.phone_number == clean_phone).first()
        if not customer:
            customer = Customer(
                phone_number=clean_phone,
                language="ur",  # Default initial language: Urdu
                conversation_state="IDLE",
                state_data="{}"
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)
        return customer

    def log_message(self, db: Session, phone_number: str, direction: str, content: str, customer_id: Optional[int] = None):
        """Record all incoming and outgoing messages in the database."""
        msg = Message(
            customer_id=customer_id,
            phone_number=phone_number,
            direction=direction,
            content=content,
            timestamp=datetime.datetime.utcnow()
        )
        db.add(msg)
        db.commit()

    def _switch_language_and_show_menu(self, db: Session, customer: Customer, new_lang: str) -> str:
        """Switch language preference and immediately display the clean localized main menu without filler text."""
        customer.language = new_lang
        customer.conversation_state = "IDLE"
        customer.state_data = "{}"
        db.commit()
        return get_text("main_menu", new_lang)

    def process_incoming_message(self, db: Session, phone_number: str, user_text: str) -> str:
        """
        Process incoming WhatsApp message through conversational state machine.
        Returns the appropriate response string in the user's selected language.
        """
        customer = self.get_or_create_customer(db, phone_number)
        raw_text = (user_text or "").strip()
        text_lower = raw_text.lower()
        lang = customer.language or "ur"

        # Log incoming customer message
        self.log_message(db, customer.phone_number, "INCOMING", raw_text, customer.id)

        # ---------------- Direct Universal Language Switchers ----------------
        if text_lower in ("urdu", "اردو", "ur", "اردو میں"):
            reply = self._switch_language_and_show_menu(db, customer, "ur")
            self.log_message(db, customer.phone_number, "OUTGOING", reply, customer.id)
            return reply

        if text_lower in ("english", "en", "eng"):
            reply = self._switch_language_and_show_menu(db, customer, "en")
            self.log_message(db, customer.phone_number, "OUTGOING", reply, customer.id)
            return reply

        if text_lower in ("sindhi", "سنڌي", "sd", "سنڌي ۾"):
            reply = self._switch_language_and_show_menu(db, customer, "sd")
            self.log_message(db, customer.phone_number, "OUTGOING", reply, customer.id)
            return reply

        # ---------------- Global Universal Reset / Cancel / Menu ----------------
        reset_keywords = (
            "0", "menu", "main menu", "مينيو", "مینیو", "cancel", "home", 
            "exit", "reset", "restart", "شروع", "دوبارہ", "منسوخ", "کینسل", "رد"
        )
        if text_lower in reset_keywords:
            customer.conversation_state = "IDLE"
            customer.state_data = "{}"
            db.commit()
            reply = get_text("main_menu", lang)
            self.log_message(db, customer.phone_number, "OUTGOING", reply, customer.id)
            return reply

        # ---------------- Universal Greetings (Always resets stale state to clean Main Menu) ----------------
        greetings = (
            "hi", "hello", "hey", "salam", "assalam", "a.o.a", "aoa", 
            "اسلام علیکم", "السلام علیکم", "سلام", "هيلو", "start"
        )
        if any(text_lower.startswith(g) for g in greetings):
            customer.conversation_state = "IDLE"
            customer.state_data = "{}"
            db.commit()
            reply = get_text("main_menu", lang)
            self.log_message(db, customer.phone_number, "OUTGOING", reply, customer.id)
            return reply

        # ---------------- Direct My Orders Query ----------------
        if text_lower in ("orders", "my orders", "میرے آرڈرز", "ہسٹری", "منظور شدہ", "منظور شدہ آرڈر", "منظور شدہ آرڈرز", "تاریخچہ", "آرڈرز", "آرڈر لسٹ"):
            reply = self._handle_my_orders(db, customer, lang)
            self.log_message(db, customer.phone_number, "OUTGOING", reply, customer.id)
            return reply

        # ---------------- Universal Direct Order Tracking by ORD Number ----------------
        if raw_text.upper().startswith("ORD-") or re.search(r"\bORD-\d{4}-\d{4}\b", raw_text.upper()):
            reply = self._handle_order_tracking(db, customer, raw_text, lang)
            self.log_message(db, customer.phone_number, "OUTGOING", reply, customer.id)
            return reply

        # ---------------- Direct Product Code Selection from IDLE State ----------------
        if (customer.conversation_state or "IDLE") == "IDLE":
            input_upper = raw_text.upper().strip()
            prod_match = db.query(Product).filter(Product.code == input_upper, Product.is_available == True).first()
            if prod_match:
                state_data = {
                    "product_id": prod_match.id,
                    "product_code": prod_match.code,
                    "product_name": prod_match.get_localized_name(lang),
                    "unit_price": prod_match.price
                }
                customer.state_data = json.dumps(state_data)
                customer.conversation_state = "ORDER_QUANTITY"
                db.commit()
                reply = get_text("ask_quantity", lang, name=prod_match.get_localized_name(lang), price=prod_match.price)
                self.log_message(db, customer.phone_number, "OUTGOING", reply, customer.id)
                return reply

        # Route by conversational state
        state = customer.conversation_state or "IDLE"

        if state == "IDLE":
            reply = self._handle_idle_state(db, customer, raw_text, lang)
        elif state == "SELECTING_LANGUAGE":
            reply = self._handle_language_selection(db, customer, raw_text)
        elif state == "ORDER_SELECT_PRODUCT":
            reply = self._handle_order_select_product(db, customer, raw_text, lang)
        elif state == "ORDER_QUANTITY":
            reply = self._handle_order_quantity(db, customer, raw_text, lang)
        elif state == "ORDER_NAME":
            reply = self._handle_order_name(db, customer, raw_text, lang)
        elif state == "ORDER_ADDRESS":
            reply = self._handle_order_address(db, customer, raw_text, lang)
        elif state == "ORDER_PAYMENT_METHOD":
            reply = self._handle_order_payment_method(db, customer, raw_text, lang)
        elif state == "ORDER_CONFIRMATION":
            reply = self._handle_order_confirmation(db, customer, raw_text, lang)
        elif state == "AWAITING_TRACKING_ID":
            reply = self._handle_order_tracking(db, customer, raw_text, lang)
        else:
            # Fallback for unexpected state: clean recovery to IDLE
            customer.conversation_state = "IDLE"
            customer.state_data = "{}"
            db.commit()
            reply = get_text("main_menu", lang)

        # Log outgoing response
        self.log_message(db, customer.phone_number, "OUTGOING", reply, customer.id)
        return reply

    # ---------------- State Handlers ----------------

    def _handle_idle_state(self, db: Session, customer: Customer, text: str, lang: str) -> str:
        """Handle top-level menu selections (1-6)."""
        choice = text.strip()

        if choice == "1":
            # 1. Browse Product Catalog (User stays in IDLE state; browsing does NOT create an order)
            products = db.query(Product).filter(Product.is_available == True).order_by(Product.id.asc()).all()
            if not products:
                return "معاف ڪجو، اسٽاڪ موجود ناهي.\nOut of stock."

            catalog_text = get_text("catalog_header", lang)
            sample_code = products[0].code if products else "P101"
            for idx, p in enumerate(products, start=1):
                name = p.get_localized_name(lang)
                desc = p.get_localized_description(lang) or "-"
                catalog_text += get_text(
                    "catalog_item", 
                    lang, 
                    index=idx, 
                    name=name, 
                    code=p.code, 
                    price=p.price, 
                    desc=desc
                )

            catalog_text += get_text("catalog_footer", lang, sample_code=sample_code)
            customer.conversation_state = "IDLE"
            customer.state_data = "{}"
            db.commit()
            return catalog_text

        elif choice == "2":
            # 2. Place New Order (Explicitly starts order flow)
            products = db.query(Product).filter(Product.is_available == True).order_by(Product.id.asc()).all()
            if not products:
                return "معاف ڪجو، اسٽاڪ موجود ناهي.\nOut of stock."

            sample_code = products[0].code if products else "P101"
            prod_lines = []
            for idx, p in enumerate(products, start=1):
                prod_lines.append(f"{idx}️⃣ *{p.get_localized_name(lang)}* (Rs {p.price:,.0f}) [ڪوڊ: `{p.code}`]")

            product_list_str = "\n".join(prod_lines)
            prompt = get_text("order_select_product_prompt", lang, sample_code=sample_code, product_list=product_list_str)

            customer.conversation_state = "ORDER_SELECT_PRODUCT"
            customer.state_data = "{}"
            db.commit()
            return prompt

        elif choice == "3":
            # 3. Track Order Status & Show Previous / Approved Orders
            orders = db.query(Order).filter(Order.customer_phone == customer.phone_number).all()
            if orders:
                return self._handle_my_orders(db, customer, lang)
            else:
                customer.conversation_state = "AWAITING_TRACKING_ID"
                db.commit()
                return get_text("ask_tracking_id", lang)

        elif choice == "4":
            # 4. Business Info & Payment Accounts
            return get_text("business_info", lang)

        elif choice == "5":
            # 5. Live Agent Handoff
            handoff = AgentHandoff(
                customer_id=customer.id,
                customer_phone=customer.phone_number,
                customer_name=customer.name,
                reason="Customer requested live human agent assistance via WhatsApp",
                status="OPEN"
            )
            db.add(handoff)
            db.commit()
            return get_text("agent_handoff", lang)

        elif choice == "6":
            # 6. Change Language
            customer.conversation_state = "SELECTING_LANGUAGE"
            db.commit()
            return get_text("select_language_prompt", lang)

        else:
            return f"{get_text('fallback_unknown', lang)}\n\n{get_text('main_menu', lang)}"

    def _handle_language_selection(self, db: Session, customer: Customer, text: str) -> str:
        """Handle language preference selection without robotic filler."""
        choice = text.strip().lower()
        if choice in ("1", "ur", "urdu", "اردو", "1️⃣"):
            return self._switch_language_and_show_menu(db, customer, "ur")
        elif choice in ("2", "en", "english", "2️⃣"):
            return self._switch_language_and_show_menu(db, customer, "en")
        elif choice in ("3", "sd", "sindhi", "سنڌي", "3️⃣"):
            return self._switch_language_and_show_menu(db, customer, "sd")
        elif choice in ("0", "cancel", "menu", "مینیو"):
            customer.conversation_state = "IDLE"
            db.commit()
            return get_text("main_menu", customer.language or "ur")
        else:
            return get_text("select_language_prompt", customer.language or "ur")

    def _handle_order_select_product(self, db: Session, customer: Customer, text: str, lang: str) -> str:
        """Validate selected product by list index or product code."""
        input_str = text.strip()
        input_upper = input_str.upper()

        if input_str in ("0", "cancel", "menu", "منسوخ", "کینسل", "رد"):
            customer.conversation_state = "IDLE"
            customer.state_data = "{}"
            db.commit()
            return get_text("order_cancelled", lang)

        # Check by product code (e.g. P101)
        product = db.query(Product).filter(
            Product.code == input_upper, 
            Product.is_available == True
        ).first()

        # If not found by code, try by numeric index (e.g. 1, 2, 3, 4, 5)
        if not product and input_str.isdigit():
            idx = int(input_str)
            all_products = db.query(Product).filter(Product.is_available == True).order_by(Product.id.asc()).all()
            if 1 <= idx <= len(all_products):
                product = all_products[idx - 1]

        if not product:
            return get_text("product_not_found", lang)

        # Store selected product in state data
        state_data = {
            "product_id": product.id,
            "product_code": product.code,
            "product_name": product.get_localized_name(lang),
            "unit_price": product.price
        }
        customer.state_data = json.dumps(state_data)
        customer.conversation_state = "ORDER_QUANTITY"
        db.commit()

        return get_text("ask_quantity", lang, name=product.get_localized_name(lang), price=product.price)

    def _handle_order_quantity(self, db: Session, customer: Customer, text: str, lang: str) -> str:
        """Process quantity input and move to customer name prompt."""
        input_str = text.strip()
        if input_str in ("0", "cancel", "menu", "منسوخ", "کینسل", "رد"):
            customer.conversation_state = "IDLE"
            customer.state_data = "{}"
            db.commit()
            return get_text("order_cancelled", lang)

        if not input_str.isdigit() or int(input_str) <= 0:
            return get_text("invalid_quantity", lang)

        quantity = int(input_str)
        try:
            state_data = json.loads(customer.state_data or "{}")
        except Exception:
            state_data = {}

        unit_price = float(state_data.get("unit_price", 0.0))
        total_amount = unit_price * quantity
        state_data["quantity"] = quantity
        state_data["total"] = total_amount
        customer.state_data = json.dumps(state_data)

        # Prompt for full name
        customer.conversation_state = "ORDER_NAME"
        db.commit()
        return get_text("ask_name", lang, quantity=quantity, total=total_amount)

    def _handle_order_name(self, db: Session, customer: Customer, text: str, lang: str) -> str:
        """Save customer name and prompt for delivery address and city."""
        input_str = text.strip()
        if input_str in ("0", "cancel", "menu", "منسوخ", "کینسل", "رد"):
            customer.conversation_state = "IDLE"
            customer.state_data = "{}"
            db.commit()
            return get_text("order_cancelled", lang)

        if len(input_str) < 2:
            return get_text("ask_name", lang, quantity=1, total=0)

        name = input_str
        customer.name = name
        try:
            state_data = json.loads(customer.state_data or "{}")
        except Exception:
            state_data = {}

        state_data["customer_name"] = name
        customer.state_data = json.dumps(state_data)

        customer.conversation_state = "ORDER_ADDRESS"
        db.commit()
        return get_text("ask_address", lang, customer_name=name)

    def _handle_order_address(self, db: Session, customer: Customer, text: str, lang: str) -> str:
        """Save delivery address and prompt for payment method choice."""
        input_str = text.strip()
        if input_str in ("0", "cancel", "menu", "منسوخ", "کینسل", "رد"):
            customer.conversation_state = "IDLE"
            customer.state_data = "{}"
            db.commit()
            return get_text("order_cancelled", lang)

        if len(input_str) < 3:
            return get_text("ask_address", lang, customer_name=customer.name or "Valued Customer")

        address = input_str
        customer.address = address
        try:
            state_data = json.loads(customer.state_data or "{}")
        except Exception:
            state_data = {}

        state_data["address"] = address
        customer.state_data = json.dumps(state_data)

        # Prompt for payment method (COD, JazzCash/EasyPaisa, Bank Transfer)
        customer.conversation_state = "ORDER_PAYMENT_METHOD"
        db.commit()
        return get_text("ask_payment_method", lang)

    def _handle_order_payment_method(self, db: Session, customer: Customer, text: str, lang: str) -> str:
        """Record customer's chosen payment method and present the complete invoice summary."""
        choice = text.strip().lower()
        if choice in ("0", "cancel", "menu", "منسوخ", "کینسل", "رد"):
            customer.conversation_state = "IDLE"
            customer.state_data = "{}"
            db.commit()
            return get_text("order_cancelled", lang)

        if choice in ("1", "cod", "cash", "1️⃣"):
            payment_method = "Cash on Delivery"
        elif choice in ("2", "jazzcash", "easypaisa", "jazz", "easy", "2️⃣"):
            payment_method = "EasyPaisa / JazzCash"
        elif choice in ("3", "bank", "transfer", "meezan", "3️⃣"):
            payment_method = "Direct Bank Transfer"
        else:
            return get_text("ask_payment_method", lang)

        try:
            state_data = json.loads(customer.state_data or "{}")
        except Exception:
            state_data = {}

        state_data["payment_method"] = payment_method
        customer.state_data = json.dumps(state_data)

        # Move to final confirmation
        customer.conversation_state = "ORDER_CONFIRMATION"
        db.commit()

        return get_text(
            "order_invoice",
            lang,
            product_name=state_data.get("product_name", "Product"),
            quantity=state_data.get("quantity", 1),
            unit_price=state_data.get("unit_price", 0.0),
            total=state_data.get("total", 0.0),
            customer_name=state_data.get("customer_name") or customer.name or "Valued Customer",
            phone=customer.phone_number,
            address=state_data.get("address") or customer.address or "Address Not Provided",
            payment_method=payment_method
        )

    def _handle_order_confirmation(self, db: Session, customer: Customer, text: str, lang: str) -> str:
        """Confirm order, write to database, and return tailored payment fulfillment details."""
        choice = text.strip().lower()

        if choice in ("1", "yes", "confirm", "ها", "ہاں", "جی", "جي", "ok", "1️⃣", "جی ہاں", "تصدیق"):
            try:
                state_data = json.loads(customer.state_data or "{}")
            except Exception:
                state_data = {}

            # Generate unique professional tracking ID: ORD-YYYY-XXXX
            year = datetime.datetime.utcnow().year
            random_num = random.randint(1000, 9999)
            order_number = f"ORD-{year}-{random_num}"

            payment_method = state_data.get("payment_method", "Cash on Delivery")
            total_amount = float(state_data.get("total", 0.0))

            # Create Order record in database
            order = Order(
                order_number=order_number,
                customer_id=customer.id,
                customer_name=state_data.get("customer_name") or customer.name or "Valued Customer",
                customer_phone=customer.phone_number,
                delivery_address=state_data.get("address") or customer.address or "Address",
                total_amount=total_amount,
                status="PENDING",
                payment_method=payment_method
            )
            db.add(order)
            db.commit()
            db.refresh(order)

            # Create OrderItem record
            order_item = OrderItem(
                order_id=order.id,
                product_id=state_data.get("product_id"),
                product_name=state_data.get("product_name") or "Product",
                unit_price=state_data.get("unit_price", 0.0),
                quantity=state_data.get("quantity", 1),
                subtotal=total_amount
            )
            db.add(order_item)

            # Reset customer state back to IDLE
            customer.conversation_state = "IDLE"
            customer.state_data = "{}"
            db.commit()

            # Return specialized payment fulfillment confirmation
            if payment_method == "EasyPaisa / JazzCash":
                return get_text("order_success_jazzcash", lang, order_number=order_number, total=total_amount)
            elif payment_method == "Direct Bank Transfer":
                return get_text("order_success_bank", lang, order_number=order_number, total=total_amount)
            else:
                return get_text("order_success_cod", lang, order_number=order_number, total=total_amount)

        elif choice in ("2", "no", "cancel", "نه", "نہیں", "2️⃣", "0", "منسوخ", "رد"):
            customer.conversation_state = "IDLE"
            customer.state_data = "{}"
            db.commit()
            return get_text("order_cancelled", lang)

        else:
            return (
                "مهرباني ڪري 1 (تصديق) يا 2 (رد) لکو:\n"
                "براہ کرم 1 (کنفرم کریں) یا 2 (منسوخ کریں) درج کریں:\n"
                "Please reply 1 (Confirm) or 2 (Cancel):"
            )

    def _handle_my_orders(self, db: Session, customer: Customer, lang: str) -> str:
        """Fetch all previous and approved orders for this customer and display structured list."""
        orders = db.query(Order).filter(Order.customer_phone == customer.phone_number).order_by(Order.created_at.desc()).limit(6).all()
        if not orders:
            customer.conversation_state = "AWAITING_TRACKING_ID"
            db.commit()
            return get_text("no_orders_found", lang)

        output = get_text("my_orders_header", lang)
        for idx, o in enumerate(orders, start=1):
            items_list = [f"{item.product_name} (x{item.quantity})" for item in o.items]
            items_str = ", ".join(items_list) if items_list else "Package"
            date_str = o.created_at.strftime("%Y-%m-%d %I:%M %p")
            status_lbl = get_status_label(o.status, lang)
            output += get_text(
                "my_orders_item",
                lang,
                idx=idx,
                order_number=o.order_number,
                status=status_lbl,
                items=items_str,
                total=o.total_amount,
                payment_method=o.payment_method,
                date=date_str
            )
        output += get_text("my_orders_footer", lang)
        customer.conversation_state = "AWAITING_TRACKING_ID"
        customer.state_data = "{}"
        db.commit()
        return output

    def _handle_order_tracking(self, db: Session, customer: Customer, text: str, lang: str) -> str:
        """Lookup order by tracking ID and return status and payment details."""
        input_term = text.strip().upper()
        if input_term in ("0", "CANCEL", "MENU", "مینیو", "مینیو"):
            customer.conversation_state = "IDLE"
            db.commit()
            return get_text("main_menu", lang)

        order = db.query(Order).filter(
            (Order.order_number == input_term) | 
            (Order.order_number.like(f"%{input_term}%"))
        ).order_by(Order.created_at.desc()).first()

        customer.conversation_state = "IDLE"
        customer.state_data = "{}"
        db.commit()

        if not order:
            return get_text("order_not_found", lang)

        # Build items list string
        items_list = [f"{item.product_name} (x{item.quantity})" for item in order.items]
        items_str = ", ".join(items_list) if items_list else "Package"
        date_str = order.created_at.strftime("%Y-%m-%d %I:%M %p")
        status_label = get_status_label(order.status, lang)

        return get_text(
            "order_status_result",
            lang,
            order_number=order.order_number,
            customer_name=order.customer_name,
            date=date_str,
            items=items_str,
            total=order.total_amount,
            payment_method=order.payment_method,
            status=status_label,
            address=order.delivery_address
        )

bot_engine = BotEngine()
