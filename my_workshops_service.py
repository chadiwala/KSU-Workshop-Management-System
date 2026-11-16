from datetime import datetime
from booking_service import get_connection


def get_my_workshops(student_id):
    with get_connection() as connection:
        return connection.execute("""
            SELECT w.workshop_id, w.name, w.location, w.date_time
            FROM bookings AS b
            JOIN workshops AS w ON b.workshop_id = w.workshop_id
            WHERE b.student_id = ? AND w.date_time > ?
            ORDER BY w.date_time
        """, (str(student_id), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))).fetchall()
