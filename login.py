import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
from pathlib import Path

from signup import SignUpWindow
from admin_window import AdminWindow
from student_window import StudentWindow
from backup_service import backup_database


DB_PATH = Path(__file__).resolve().parent / "ksu_workshop.db"


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("KSU Workshop - Login")
        self.root.geometry("400x350")
        self.root.config(bg="#f5f6fa")

        self.open_signup()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_page(self):
        self.clear_window()

        self.root.title("KSU Workshop - Login")
        self.root.geometry("400x350")
        self.root.config(bg="#f5f6fa")

        tk.Label(
            self.root,
            text="KSU Workshop Login",
            font=("Arial", 16, "bold"),
            bg="#f5f6fa"
        ).pack(pady=20)

        tk.Label(
            self.root,
            text="Student / Admin ID",
            bg="#f5f6fa"
        ).pack(pady=5)

        self.id_entry = tk.Entry(self.root, width=30)
        self.id_entry.pack(pady=5)

        tk.Label(
            self.root,
            text="Password",
            bg="#f5f6fa"
        ).pack(pady=5)

        self.password_entry = tk.Entry(
            self.root,
            width=30,
            show="*"
        )
        self.password_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="Login",
            command=self.login,
            bg="#27ae60",
            fg="white",
            width=15
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Sign Up",
            command=self.open_signup,
            bg="#2980b9",
            fg="white",
            width=15
        ).pack(pady=5)

    def login(self):
        user_id = self.id_entry.get().strip()
        password = self.password_entry.get()

        # Input Validation
        if not user_id or not password:
            messagebox.showerror(
                "Error",
                "Please enter your ID and Password"
            )
            return

        if not user_id.isascii() or not user_id.isdigit() or len(user_id) != 9:
            messagebox.showerror(
                "Error",
                "ID must contain exactly 9 digits"
            )
            return

        # Password Hash
        password_hash = hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()

                # Check Student
                cursor.execute(
                    """SELECT student_id
                       FROM students
                       WHERE student_id = ?
                       AND password_hash = ?""",
                    (user_id, password_hash)
                )

                student = cursor.fetchone()

                if student:
                    user_role = "student"
                else:
                    # Check Admin
                    cursor.execute(
                        """SELECT admin_id
                           FROM admins
                           WHERE admin_id = ?
                           AND password_hash = ?""",
                        (user_id, password_hash)
                    )

                    admin = cursor.fetchone()
                    user_role = "admin" if admin else None

            # Open Student Window
            if user_role == "student":
                messagebox.showinfo(
                    "Success",
                    "Student login successful!"
                )

                self.clear_window()

                StudentWindow(
                    self.root,
                    student_id=user_id,
                    on_logout=self.open_signup
                )
                return

            # Open Admin Window
            if user_role == "admin":
                messagebox.showinfo(
                    "Success",
                    "Admin login successful!"
                )

                self.clear_window()

                self.root.withdraw()
                self.admin_window = AdminWindow(
                    self.root,
                    on_logout=self.open_signup,
                    on_backup=backup_database
                )
                return

            # Invalid Login
            messagebox.showerror(
                "Login Failed",
                "Invalid ID or Password"
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    def open_signup(self):
        self.clear_window()
        self.root.deiconify()

        SignUpWindow(
            self.root,
            on_switch_to_login=self.create_login_page
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()