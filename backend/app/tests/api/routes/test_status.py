from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_accept_order_bad():
    resp = client.post("/api/v1/orders/00000000-0000-0000-0000-000000000000/accept?driver_id=11111111-1111-1111-1111-111111111111")
    assert resp.status_code in (400, 404)
