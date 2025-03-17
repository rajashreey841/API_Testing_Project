import requests
import pytest

BASE_URL = "https://restful-booker.herokuapp.com"

# Function to Generate Token
def get_token():
    auth_data = {"username": "admin", "password": "password123"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/auth", json=auth_data, headers=headers)
    assert response.status_code == 200, f"Failed to generate token: {response.text}"
    return response.json()["token"]

TOKEN = get_token()


# Function to Create Booking (Used by Multiple Tests)
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
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.post(f"{BASE_URL}/booking", json=data, headers=headers)
    assert response.status_code == 200, f"Booking creation failed: {response.text}"
    return response.json()["bookingid"]  # Return the ID for reuse


# Test Case: Create Booking
def test_create_booking():
    booking_id = create_booking()
    assert isinstance(booking_id, int), "Booking ID should be an integer"


# Test Case: Get All Bookings
def test_get_all_bookings():
    response = requests.get(f"{BASE_URL}/booking")
    assert response.status_code == 200, f"Failed to get bookings: {response.text}"
    assert isinstance(response.json(), list)


# Test Case: Get Booking by ID
def test_get_booking_by_id():
    booking_id = create_booking()  # Use a valid dynamic ID
    response = requests.get(f"{BASE_URL}/booking/{booking_id}")
    assert response.status_code == 200, f"Booking not found: {response.text}"
    data = response.json()
    assert "firstname" in data
    assert "lastname" in data


# Test Case: Update Booking
def test_update_booking():
    booking_id = create_booking()  # Use a valid dynamic ID
    data = {
        "firstname": "Rajashree",
        "lastname": "UpdatedName",
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-15"
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={TOKEN}"
    }
    response = requests.put(f"{BASE_URL}/booking/{booking_id}", json=data, headers=headers)
    assert response.status_code == 200, f"Update failed: {response.text}"
    updated_data = response.json()
    assert updated_data["firstname"] == "Rajashree"
    assert updated_data["lastname"] == "UpdatedName"


# Test Case: Delete Booking
def test_delete_booking():
    booking_id = create_booking()  # Use a valid dynamic ID
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"token={TOKEN}"
    }
    response = requests.delete(f"{BASE_URL}/booking/{booking_id}", headers=headers)
    assert response.status_code in [201, 204], f"Delete failed: {response.text}"


# Test Case: Validate Response Structure
def test_response_structure():
    booking_id = create_booking()  # Use a valid dynamic ID
    response = requests.get(f"{BASE_URL}/booking/{booking_id}")
    assert response.status_code == 200, f"Response failed: {response.text}"
    data = response.json()
    assert all(key in data for key in ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"])


# Test Case: Invalid Booking ID
def test_invalid_booking_id():
    invalid_booking_id = 99999999  # High value to ensure it's invalid
    response = requests.get(f"{BASE_URL}/booking/{invalid_booking_id}")
    assert response.status_code == 404, f"Expected 404, but got {response.status_code}"
    assert "Not Found" in response.text


# Entry point to run all tests
if __name__ == "__main__":
    pytest.main(["-v", "test_api.py"])

