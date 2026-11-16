
import random
from contextlib import closing
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / 'ksu_workshop.db'


def initialize_database(db_path=DB_PATH):
    with closing(sqlite3.connect(str(db_path))) as connection:
        connection.execute('''
            CREATE TABLE IF NOT EXISTS workshops (
                workshop_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                capacity INTEGER NOT NULL CHECK (capacity > 0),
                date_time TEXT NOT NULL,
                current_bookings INTEGER NOT NULL DEFAULT 0
                    CHECK (current_bookings >= 0)
            )
        ''')


def validate_workshop(name, location, capacity, workshop_date, workshop_time):
    name, location = name.strip(), location.strip()
    capacity, workshop_date, workshop_time = (
        capacity.strip(), workshop_date.strip(), workshop_time.strip()
    )

    if not name:
        raise ValueError('Please enter the workshop name.')

    if not location:
        raise ValueError('Please enter the workshop location.')

    if not capacity.isdigit() or int(capacity) <= 0:
        raise ValueError('Capacity must be a positive integer.')

    date_time_text = workshop_date + ' ' + workshop_time

    try:
        parsed = datetime.strptime(date_time_text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError(
            'Enter a valid date and time (YYYY-MM-DD and HH:MM).'
        ) from None

    if parsed.strftime('%Y-%m-%d %H:%M') != date_time_text:
        raise ValueError(
            'Use date YYYY-MM-DD and time HH:MM (24-hour format).'
        )

    return name, location, int(capacity), date_time_text


def create_workshop(name, location, capacity, workshop_date, workshop_time,
                    db_path=DB_PATH):

    name, location, capacity, date_time_text = validate_workshop(
        name, location, capacity, workshop_date, workshop_time
    )

    initialize_database(db_path)

    with closing(sqlite3.connect(str(db_path))) as connection:
        for _ in range(100):
            workshop_id = random.randint(10000, 99999)

            exists = connection.execute(
                'SELECT 1 FROM workshops WHERE workshop_id = ?',
                (workshop_id,)
            ).fetchone()

            if exists:
                continue

            try:
                connection.execute('''
                    INSERT INTO workshops
                    (workshop_id, name, location, capacity, date_time, current_bookings)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    workshop_id, name, location,
                    capacity, date_time_text, 0
                ))

                connection.commit()
                return workshop_id

            except sqlite3.IntegrityError:
                if connection.execute(
                    'SELECT 1 FROM workshops WHERE workshop_id = ?',
                    (workshop_id,)
                ).fetchone():
                    continue
                raise

    raise RuntimeError(
        'Could not generate a unique workshop ID. Please try again.'
    )
