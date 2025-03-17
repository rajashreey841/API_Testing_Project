import requests

BASE_URL = "https://restful-booker.herokuapp.com"


# Step 1: Generate Authentication Token
def get_token():
    auth_data = {"username": "admin", "password": "password123"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/auth", json=auth_data, headers=headers)
    assert response.status_code == 200, f"Failed to generate token: {response.text}"
    return response.json()["token"]


TOKEN = get_token()


# Step 2: Create Booking First
def create_booking():
    data = {
        "firstname": "Rajashree",
        "lastname": "QA",
        "totalprice": 200,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-01-01",
            "checkout": "2025-01-10"
        }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/booking", json=data, headers=headers)
    assert response.status_code == 200
    return response.json()["bookingid"]


# Step 3: Delete the Created Booking
def test_delete_booking():
    booking_id = create_booking()  # Ensure booking exists before deleting
    
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"token={TOKEN}",
        "Accept": "application/json"
    }
    
    response = requests.delete(f"{BASE_URL}/booking/{booking_id}", headers=headers)
    
    assert response.status_code == 201, f"Failed to delete booking: {response.text}"



