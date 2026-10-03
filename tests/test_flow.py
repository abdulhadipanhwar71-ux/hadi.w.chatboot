"""
Automated unit tests for bot conversation engine, orders, and multilingual switching.
All comments and code are strictly in English.
"""

import sys
import re
from pathlib import Path

# Add project root directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal
from app.services.bot_engine import bot_engine
from app.models import Order, Customer, Message, AgentHandoff

def test_full_bot_flow():
    db = SessionLocal()
    test_phone = "923119998877"
    
    # Reset customer test state to Sindhi for testing
    cust = bot_engine.get_or_create_customer(db, test_phone)
    cust.language = "sd"
    cust.conversation_state = "IDLE"
    cust.state_data = "{}"
    db.commit()

    print("--- 1. Testing Initial Greeting & Sindhi Menu ---")
    reply1 = bot_engine.process_incoming_message(db, test_phone, "سلام")
    assert "ڀلي ڪري آيا" in reply1, "Greeting should contain Sindhi welcome"
    print("PASS: Greeting & Sindhi Menu received.")

    print("\n--- 2. Testing Product Catalog Display ---")
    reply2 = bot_engine.process_incoming_message(db, test_phone, "1")
    assert "پروڊڪٽس" in reply2, "Catalog should be in Sindhi"
    assert "اجرڪ" in reply2 or "P101" in reply2, "Should list Sindhi products"
    print("PASS: Product Catalog displayed successfully.")

    print("\n--- 3. Testing Order Placement Flow ---")
    # Step 1: Select product P101
    reply_ord1 = bot_engine.process_incoming_message(db, test_phone, "P101")
    assert "توهان چونڊيو آهي" in reply_ord1, "Should acknowledge product selection"
    print("Step 3.1: Product selected.")

    # Step 2: Quantity
    reply_ord2 = bot_engine.process_incoming_message(db, test_phone, "2")
    assert "پورو نالو" in reply_ord2, "Should request customer full name"
    print("Step 3.2: Quantity accepted.")

    # Step 3: Full Name
    reply_ord3 = bot_engine.process_incoming_message(db, test_phone, "علي نواز سنڌي")
    assert "ترسيل پتو" in reply_ord3, "Should ask for delivery address"
    print("Step 3.3: Name accepted.")

    # Step 4: Delivery Address
    reply_ord4 = bot_engine.process_incoming_message(db, test_phone, "قاسم آباد، حيدرآباد، سنڌ")
    assert "ادائگي جو طريقو" in reply_ord4, "Should display payment method selection"
    print("Step 3.4: Address accepted & payment methods displayed.")

    # Step 5: Payment Method (1 = COD)
    reply_ord5 = bot_engine.process_incoming_message(db, test_phone, "1")
    assert "رسيد ۽ تفصيل" in reply_ord5, "Should display order confirmation invoice"
    print("Step 3.5: Payment method selected & invoice displayed.")

    # Step 6: Confirm Order (1 = Confirm)
    reply_ord6 = bot_engine.process_incoming_message(db, test_phone, "1")
    assert "مبارڪ هجي" in reply_ord6, "Should confirm order successfully"
    
    # Extract order number
    match = re.search(r"ORD-\d{4}-\d{4}", reply_ord6)
    assert match is not None, "Order ID format should match ORD-YYYY-XXXX"
    order_num = match.group(0)
    print(f"Step 3.6: Order placed successfully with ID: {order_num}")

    # Verify in DB
    order_db = db.query(Order).filter(Order.order_number == order_num).first()
    assert order_db is not None, "Order must exist in database"
    assert order_db.customer_phone == test_phone
    assert order_db.total_amount == 5000.0  # 2500 * 2
    assert order_db.payment_method == "Cash on Delivery"
    print(f"PASS: Verified order in DB with amount Rs {order_db.total_amount} and COD.")

    print("\n--- 4. Testing Order Status Tracking ---")
    status_reply = bot_engine.process_incoming_message(db, test_phone, order_num)
    assert order_num in status_reply
    assert "علي نواز سنڌي" in status_reply
    print(f"PASS: Order status tracked correctly.")

    print("\n--- 5. Testing Language Switch to Urdu ---")
    lang_reply = bot_engine.process_incoming_message(db, test_phone, "اردو") # Direct Urdu switch
    assert "ہمارے واٹس ایپ اسٹور میں خوش آمدید" in lang_reply
    print("PASS: Switched language to Urdu cleanly.")

    print("\n--- 6. Testing Language Switch to English ---")
    lang_reply_en = bot_engine.process_incoming_message(db, test_phone, "english") # Direct English switch
    assert "Welcome to our WhatsApp Store" in lang_reply_en
    print("PASS: Switched language to English cleanly.")

    print("\n--- 7. Testing Agent Handoff ---")
    handoff_reply = bot_engine.process_incoming_message(db, test_phone, "5") # Human agent
    assert "representative" in handoff_reply.lower() or "support" in handoff_reply.lower()
    handoff_db = db.query(AgentHandoff).filter(AgentHandoff.customer_phone == test_phone).order_by(AgentHandoff.id.desc()).first()
    assert handoff_db is not None
    assert handoff_db.status == "OPEN"
    print("PASS: Human Agent request ticket created in database.")

    db.close()
    print("\n>>> ALL BOT FLOW TESTS PASSED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    test_full_bot_flow()
