import requests

BASE_URL = "https://restful-booker.herokuapp.com"

def test_get_booking():
    response = requests.get(f"{BASE_URL}/booking/1")
    assert response.status_code == 200
    assert "firstname" in response.json()

def test_create_booking():
    data = {
        "firstname": "Rajashree",
        "lastname": "QA",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-01-01",
            "checkout": "2025-01-10"
        }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/booking", json=data, headers=headers)
    assert response.status_code == 200
    assert "bookingid" in response.json()

