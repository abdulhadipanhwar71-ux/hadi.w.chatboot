"""
Web endpoints integration test.
All comments and code are strictly in English.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_endpoints():
    print("Testing GET / ...")
    r = client.get("/", follow_redirects=False)
    assert r.status_code in (302, 303, 307)
    print("PASS: / redirects to /admin.")

    print("Testing GET /admin ...")
    r = client.get("/admin")
    assert r.status_code == 200
    assert "Business Overview Dashboard" in r.text
    print("PASS: Admin Dashboard loads.")

    print("Testing GET /admin/orders ...")
    r = client.get("/admin/orders")
    assert r.status_code == 200
    assert "Orders Management" in r.text
    print("PASS: Orders Management loads.")

    print("Testing GET /admin/products ...")
    r = client.get("/admin/products")
    assert r.status_code == 200
    assert "Product Catalog" in r.text
    print("PASS: Product Catalog loads.")

    print("Testing GET /admin/customers ...")
    r = client.get("/admin/customers")
    assert r.status_code == 200
    assert "Customer Directory" in r.text
    print("PASS: Customers Directory loads.")

    print("Testing GET /simulator ...")
    r = client.get("/simulator")
    assert r.status_code == 200
    assert "Business WhatsApp Bot" in r.text
    print("PASS: Live Simulator loads.")

    print("Testing POST /simulator/send ...")
    r = client.post("/simulator/send", json={"phone_number": "923451122334", "message": "سلام"})
    assert r.status_code == 200
    data = r.json()
    assert "ڀلي ڪري آيا" in data["reply"]
    print("PASS: Simulator send API responds with authentic Sindhi welcome.")

    print("Testing GET /webhook verification ...")
    r = client.get("/webhook?hub.mode=subscribe&hub.challenge=meta_challenge_777&hub.verify_token=my_secure_webhook_verify_token_123")
    assert r.status_code == 200
    assert r.text == "meta_challenge_777"
    print("PASS: WhatsApp Webhook verification handshake succeeds.")

    print("\n>>> ALL WEB & API ENDPOINTS VERIFIED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    test_endpoints()
