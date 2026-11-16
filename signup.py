import sqlite3
import hashlib
import re
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "ksu_workshop.db"

class SignUpWindow:
    def __init__(self, root, on_switch_to_login=None):
        self.root = root
        self.root.title("KSUWorkshop - Student Sign Up")
        self.root.geometry("450x650")
        self.root.config(bg="#f5f6fa")
        self.on_switch_to_login = on_switch_to_login

        self.init_db()

        title_label = tk.Label(root, text="Student Sign Up", font=("Arial", 16, "bold"), bg="#f5f6fa", fg="#2c3e50")
        title_label.pack(pady=20)

        form_frame = tk.Frame(root, bg="#f5f6fa")
        form_frame.pack(pady=10, padx=30, fill="x")

        # First Name
        tk.Label(form_frame, text="First Name:", bg="#f5f6fa", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
        self.first_name_entry = tk.Entry(form_frame, font=("Arial", 11), width=35)
        self.first_name_entry.pack(fill="x", pady=4)

        # Last Name
        tk.Label(form_frame, text="Last Name:", bg="#f5f6fa", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
        self.last_name_entry = tk.Entry(form_frame, font=("Arial", 11), width=35)
        self.last_name_entry.pack(fill="x", pady=4)

        # Student ID
        tk.Label(form_frame, text="Student ID (9 digits):", bg="#f5f6fa", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
        self.id_entry = tk.Entry(form_frame, font=("Arial", 11), width=35)
        self.id_entry.pack(fill="x", pady=4)

        # Email
        tk.Label(form_frame, text="Email (XXXXXXXX@student.ksu.edu.sa):", bg="#f5f6fa", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
        self.email_entry = tk.Entry(form_frame, font=("Arial", 11), width=35)
        self.email_entry.pack(fill="x", pady=4)

        # Phone
        tk.Label(form_frame, text="Phone Number (05XXXXXXXX):", bg="#f5f6fa", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
        self.phone_entry = tk.Entry(form_frame, font=("Arial", 11), width=35)
        self.phone_entry.pack(fill="x", pady=4)

        # Password
        tk.Label(form_frame, text="Password (at least 6 characters):", bg="#f5f6fa", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
        self.password_entry = tk.Entry(form_frame, font=("Arial", 11), width=35, show="*")
        self.password_entry.pack(fill="x", pady=4)

        # Buttons Frame
        btn_frame = tk.Frame(root, bg="#f5f6fa")
        btn_frame.pack(pady=20)

        submit_btn = tk.Button(btn_frame, text="Submit", font=("Arial", 11, "bold"), bg="#27ae60", fg="white", width=14, command=self.register_student)
        submit_btn.grid(row=0, column=0, padx=8)

        login_btn = tk.Button(btn_frame, text="Login", font=("Arial", 11), bg="#2980b9", fg="white", width=14, command=self.open_login)
        login_btn.grid(row=0, column=1, padx=8)

    def init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def validate_inputs(self, first_name, last_name, student_id, email, phone, password):
        if not all([first_name, last_name, student_id, email, phone, password]):
            messagebox.showerror("Validation Error", "All fields are required!")
            return False

        if not re.fullmatch(r'[0-9]{9}', student_id):
            messagebox.showerror("Validation Error", "Student ID must be exactly 9 digits.")
            return False

        # Updated email regex
        if not re.fullmatch(r'[A-Za-z0-9]{8}@student\.ksu\.edu\.sa', email):
            messagebox.showerror("Validation Error", "Email must be in the format: XXXXXXXX@student.ksu.edu.sa")
            return False

        if not re.fullmatch(r'05[0-9]{8}', phone):
            messagebox.showerror("Validation Error", "Phone number must start with 05 and be 10 digits (05XXXXXXXX).")
            return False

        if not re.fullmatch(r'[A-Za-z0-9]{6,}', password):
            messagebox.showerror("Validation Error", "Password must contain at least 6 letters or digits.")
            return False

        return True

    def register_student(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        student_id = self.id_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        password = self.password_entry.get().strip()

        if not self.validate_inputs(first_name, last_name, student_id, email, phone, password):
            return

        pwd_hash = self.hash_password(password)

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM students WHERE student_id = ? OR email = ?", (student_id, email))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror("Registration Error", "Student ID or Email is already registered!")
                conn.close()
                return

            cursor.execute('''
                INSERT INTO students (student_id, first_name, last_name, email, phone, password_hash)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, first_name, last_name, email, phone, pwd_hash))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Account created successfully!")
            self.clear_fields()

            if self.on_switch_to_login:
                self.on_switch_to_login()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def clear_fields(self):
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def open_login(self):
        if self.on_switch_to_login:
            self.on_switch_to_login()
        else:
            messagebox.showinfo("Navigation", "Login window switch hook not provided.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SignUpWindow(root)
    root.mainloop()