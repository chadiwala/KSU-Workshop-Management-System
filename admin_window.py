
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from workshop_db import create_workshop, initialize_database


class AdminWindow(tk.Toplevel):

    def __init__(self, master, on_logout=None, on_backup=None):
        super().__init__(master)

        self.on_logout = on_logout
        self.on_backup = on_backup

        self.title('KSUWorkshop | Admin')
        self.geometry('700x700')
        self.minsize(600, 680)
        self.configure(bg='#f3f6fc')
        self.protocol('WM_DELETE_WINDOW', self.logout)

        self.name_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.capacity_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.time_var = tk.StringVar()

        self.status_var = tk.StringVar(
            value='Fill in the form to create a workshop.'
        )

        self.build_gui()
        initialize_database()

    def add_field(self, parent, label, variable):
        box = tk.Frame(parent, bg='white')
        box.pack(fill='x', pady=(0, 6))

        tk.Label(
            box,
            text=label,
            bg='white',
            fg='#294260',
            font=('Segoe UI', 10, 'bold')
        ).pack(anchor='w', pady=(0, 2))

        entry = ttk.Entry(
            box,
            textvariable=variable,
            font=('Segoe UI', 11)
        )

        entry.pack(fill='x', ipady=3)
        return entry

    def build_gui(self):
        style = ttk.Style(self)
        style.configure('TEntry', padding=5)

        header = tk.Frame(
            self,
            bg='#173b73',
            height=94
        )
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(
            header,
            text='KSUWorkshop',
            bg='#173b73',
            fg='white',
            font=('Segoe UI', 24, 'bold')
        ).pack(pady=(13, 2))

        tk.Label(
            header,
            text='ADMIN  |  WORKSHOP MANAGEMENT',
            bg='#173b73',
            fg='#d2e2f7',
            font=('Segoe UI', 10, 'bold')
        ).pack()

        card = tk.Frame(
            self,
            bg='white',
            padx=30,
            pady=12,
            highlightbackground='#dbe3ef',
            highlightthickness=1
        )
        card.pack(
            fill='both',
            expand=True,
            padx=43,
            pady=(14, 8)
        )

        tk.Label(
            card,
            text='Create a Workshop',
            bg='white',
            fg='#173b73',
            font=('Segoe UI', 18, 'bold')
        ).pack(anchor='w', pady=(0, 9))

        self.name_entry = self.add_field(
            card, 'Workshop Name', self.name_var
        )

        self.add_field(
            card, 'Location', self.location_var
        )

        self.add_field(
            card, 'Capacity (positive integer)', self.capacity_var
        )

        self.add_field(
            card, 'Date (YYYY-MM-DD)', self.date_var
        )

        self.add_field(
            card, 'Time (HH:MM, 24-hour format)', self.time_var
        )

        tk.Button(
            card,
            text='Create Workshop',
            command=self.create,
            font=('Segoe UI', 12, 'bold'),
            bg='#1462b3',
            fg='white',
            activebackground='#114f90',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            pady=7
        ).pack(fill='x', pady=(0, 8))

        tk.Label(
            card,
            textvariable=self.status_var,
            bg='white',
            fg='#267441',
            font=('Segoe UI', 10),
            wraplength=550
        ).pack(anchor='w', pady=(0, 7))

        tk.Frame(
            card,
            height=1,
            bg='#e3eaf3'
        ).pack(fill='x', pady=(0, 8))

        bottom = tk.Frame(card, bg='white')
        bottom.pack(fill='x')

        tk.Button(
            bottom,
            text='Backup',
            command=self.backup,
            font=('Segoe UI', 11),
            bg='#eaf0f8',
            fg='#173b73',
            relief='flat',
            cursor='hand2',
            pady=7
        ).pack(
            side='left',
            fill='x',
            expand=True,
            padx=(0, 7)
        )

        tk.Button(
            bottom,
            text='Logout',
            command=self.logout,
            font=('Segoe UI', 11),
            bg='#eaf0f8',
            fg='#173b73',
            relief='flat',
            cursor='hand2',
            pady=7
        ).pack(
            side='left',
            fill='x',
            expand=True,
            padx=(7, 0)
        )

        tk.Label(
            self,
            text='King Saud University  |  KSUWorkshop',
            bg='#f3f6fc',
            fg='#718096',
            font=('Segoe UI', 9)
        ).pack(pady=(0, 8))

        self.name_entry.focus_set()

    def create(self):
        try:
            workshop_id = create_workshop(
                self.name_var.get(),
                self.location_var.get(),
                self.capacity_var.get(),
                self.date_var.get(),
                self.time_var.get()
            )

        except ValueError as error:
            messagebox.showerror(
                'Invalid Input', str(error), parent=self
            )
            return

        except (sqlite3.Error, RuntimeError) as error:
            messagebox.showerror(
                'Database Error', str(error), parent=self
            )
            return

        self.status_var.set(
            'Workshop #' + str(workshop_id) +
            ' created successfully! Current bookings: 0'
        )

        messagebox.showinfo(
            'Success',
            'Workshop created!\nWorkshop ID: ' + str(workshop_id),
            parent=self
        )

        self.name_var.set('')
        self.location_var.set('')
        self.capacity_var.set('')
        self.date_var.set('')
        self.time_var.set('')

        self.name_entry.focus_set()

    def backup(self):
        if self.on_backup is None:
            messagebox.showinfo(
                'Backup Integration',
                'The Backup button is ready. The CSV export function '
                'will be connected to teammate 5\'s code.',
                parent=self
            )
            return

        try:
            backup_path = self.on_backup()

        except Exception as error:
            messagebox.showerror(
                'Backup Error', str(error), parent=self
            )
            return

        if backup_path:
            messagebox.showinfo(
                'Backup Complete',
                'Backup saved to:\n' + str(backup_path),
                parent=self
            )

    def logout(self):
        self.destroy()

        if self.on_logout is not None:
            self.on_logout()

        elif self.master is not None:
            self.master.destroy()
