import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "ksu_workshop.db"

conn = sqlite3.connect(str(DB_PATH))

conn.execute("PRAGMA foreign_keys = ON")

conn.executescript("""

CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS admins (
    admin_id TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS workshops (
    workshop_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    date_time TEXT NOT NULL,
    current_bookings INTEGER NOT NULL DEFAULT 0
        CHECK (current_bookings >= 0)
);

CREATE TABLE IF NOT EXISTS bookings (
    student_id TEXT NOT NULL,
    workshop_id INTEGER NOT NULL,
    booked_at TEXT NOT NULL,

    PRIMARY KEY (student_id, workshop_id),

    FOREIGN KEY (student_id)
        REFERENCES students(student_id),

    FOREIGN KEY (workshop_id)
        REFERENCES workshops(workshop_id)
);

""")

conn.commit()

print("Database created successfully!")

for row in conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
):
    print(row[0])

conn.close()