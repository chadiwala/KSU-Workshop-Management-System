"""Student booking logic using the team's existing SQLite schema."""
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / 'ksu_workshop.db'


def get_connection():
    connection = sqlite3.connect(str(DB_PATH), timeout=10)
    connection.execute('PRAGMA foreign_keys = ON')
    return connection


def get_workshops():
    with get_connection() as connection:
        return connection.execute('''
            SELECT workshop_id, name, location, date_time, capacity, current_bookings
            FROM workshops WHERE date_time > ? ORDER BY date_time
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),)).fetchall()


def book_workshop(student_id, workshop_id):
    connection = get_connection()
    try:
        # Lock before checking seats so two bookings cannot take the last seat.
        connection.execute('BEGIN IMMEDIATE')
        student = connection.execute('SELECT student_id FROM students WHERE student_id = ?',
                                     (str(student_id),)).fetchone()
        if student is None:
            connection.rollback()
            return False, 'Student account not found. Please log in again.'

        workshop = connection.execute('''
            SELECT capacity, current_bookings, date_time FROM workshops WHERE workshop_id = ?
        ''', (workshop_id,)).fetchone()
        if workshop is None:
            connection.rollback()
            return False, 'Workshop not found.'

        capacity, booked, date_time = workshop
        try:
            workshop_time = datetime.fromisoformat(date_time)
        except ValueError:
            connection.rollback()
            return False, 'Workshop date has an invalid format.'
        if workshop_time <= datetime.now():
            connection.rollback()
            return False, 'This workshop is no longer active.'

        already_booked = connection.execute('''
            SELECT 1 FROM bookings WHERE student_id = ? AND workshop_id = ?
        ''', (str(student_id), workshop_id)).fetchone()
        if already_booked:
            connection.rollback()
            return False, 'You already booked this workshop.'
        if booked >= capacity:
            connection.rollback()
            return False, 'This workshop is full.'

        connection.execute('''
            INSERT INTO bookings (student_id, workshop_id, booked_at) VALUES (?, ?, ?)
        ''', (str(student_id), workshop_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        connection.execute('''
            UPDATE workshops SET current_bookings = current_bookings + 1 WHERE workshop_id = ?
        ''', (workshop_id,))
        connection.commit()
        return True, 'Workshop booked successfully!'
    except sqlite3.Error:
        connection.rollback()
        raise
    finally:
        connection.close()
