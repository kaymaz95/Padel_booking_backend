from fastapi.testclient import TestClient
from api import app
from booking import bookings
import pytest

@pytest.fixture(autouse=True)
def clear_bookings():
    bookings.clear()

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "padel-booking"}

def test_get_unknown_customer():
    response = client.get("/bookings/Zara")
    assert response.status_code == 404
    assert response.json() == {"detail": "Customer not found"}

def test_create_and_get_booking():
    response = client.post("/bookings", json={"customer": "Karl",
                                              "court":1,
                                              "start_time":"14:00",
                                              "duration":30
                                              })
    assert response.status_code == 200
    booking = response.json()
    assert booking["customer"] == "Karl"
    assert booking["court"] == 1
    assert booking["confirmed"]== True
    assert booking["duration"] == 30

    get_response = client.get("/bookings/Karl")
    assert get_response.status_code == 200
    assert get_response.json() == booking