<div align="center">
  <img src="assets/E2356DBC-76B8-42AF-BBD4-47229FFCB186.gif" width="100%" alt="KSU Workshop Management System Animated Banner">
</div>

# 🎓 KSU Workshop Management System

### A Python desktop application for university workshop scheduling and student bookings

**Python** · **Tkinter** · **SQLite** · **CSV Export**

</div>

---

## Overview

KSU Workshop Management System is a university team project that brings workshop administration and student registration into a single desktop application. It provides separate student and administrator interfaces backed by a local SQLite database.

## Features

| Student experience | Administrator experience |
| --- | --- |
| Register and sign in | Sign in to the admin portal |
| Browse upcoming workshops | Create and manage workshop listings |
| Book available seats | View workshop information |
| Review upcoming bookings | Export database tables to CSV |

The booking service checks seat availability inside a SQLite transaction to reduce conflicting reservations.

## Technology

- **Python 3** — application logic
- **Tkinter / ttk** — desktop user interface (included with many Python distributions)
- **SQLite** — local relational database
- **CSV** — data export and backups

## Getting started

1. Install Python 3 with Tkinter support.
2. Clone or download this repository.
3. Open a terminal in the project directory.
4. Initialize the database:

   ```bash
   python setup_database.py
   ```

5. Launch the desktop application:

   ```bash
   python login.py
   ```

> The app uses a local `ksu_workshop.db` file, which is deliberately excluded from version control. The database is created using the supplied setup script. No external Python packages are required by the current source files.

## Project structure

```text
KSU-Workshop-Management-System/
├── login.py                 # Entry point and authentication flow
├── signup.py                # Student registration
├── student_window.py        # Student dashboard
├── admin_window.py          # Administrator dashboard
├── booking_service.py       # Seat reservation logic
├── my_workshops_service.py  # Student booking queries
├── workshop_db.py           # Workshop database operations
├── setup_database.py        # Database schema initialization
├── backup_service.py        # CSV data export
├── docs/
│   └── screenshots/         # Add actual UI captures here
├── .gitignore
└── README.md
```

## Database design

The SQLite schema includes four tables:

- `students` — student accounts
- `admins` — administrator accounts
- `workshops` — scheduled workshops and capacities
- `bookings` — student-to-workshop reservations

## Screenshots

Screenshots of the real application can be added to `docs/screenshots/` and linked here. No mock screenshots are presented as real captures.

## Project context and credits

Developed as a **collaborative university Python project**. Contributions belong to the respective team members. Add the team's agreed names, roles, and attribution before publishing a final contributor list.

## Notes

- Designed as a local desktop application, not a hosted website.
- The provided database is not included because it contains account and booking records.
- This repository is a learning project; review security and data handling before production use.
