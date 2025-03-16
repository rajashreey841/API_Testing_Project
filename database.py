import sqlite3

def check_booking_in_db(booking_id):
    conn = sqlite3.connect("bookings.db")  
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM bookings WHERE id={booking_id}")
    result = cursor.fetchone()
    conn.close()
    return result is not None

