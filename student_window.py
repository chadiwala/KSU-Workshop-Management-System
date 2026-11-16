"""Student 4: Tkinter booking tab; Student 5 supplies View My Workshops."""

import sqlite3
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from booking_service import get_workshops, book_workshop
from my_workshops_service import get_my_workshops

BLUE = '#205A9F'
DARK = '#163C68'
BG = '#F1F5FA'


class StudentWindow(ttk.Frame):
    def __init__(self, master, student_id, on_logout=None):
        super().__init__(master, padding=16)
        self.student_id = str(student_id)
        self.on_logout = on_logout

        master.title('KSUWorkshop - Student Portal')
        master.geometry('1050x630')
        master.minsize(800, 500)

        self.pack(fill='both', expand=True)

        style = ttk.Style(master)
        style.configure(
            'Title.TLabel',
            font=('Arial', 22, 'bold'),
            foreground=DARK
        )
        style.configure(
            'Section.TLabel',
            font=('Arial', 15, 'bold'),
            foreground=DARK
        )
        style.configure(
            'Info.TLabel',
            font=('Arial', 10),
            foreground='#536A82'
        )
        style.configure(
            'Book.TButton',
            font=('Arial', 11, 'bold'),
            padding=10
        )
        style.configure(
            'Treeview',
            font=('Arial', 10),
            rowheight=32
        )
        style.configure(
            'Treeview.Heading',
            font=('Arial', 10, 'bold')
        )

        # Header with visible Logout button
        header = ttk.Frame(self)
        header.pack(fill='x')

        ttk.Label(
            header,
            text='KSUWorkshop',
            style='Title.TLabel'
        ).pack(side='left')

        ttk.Button(
            header,
            text='Logout',
            command=self.logout
        ).pack(side='right')

        ttk.Label(
            self,
            text='Workshop Management System  |  Student ID: ' + self.student_id,
            style='Info.TLabel'
        ).pack(anchor='w', pady=(0, 15))

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill='both', expand=True)

        self.book_tab = ttk.Frame(self.tabs, padding=14)
        self.my_tab = ttk.Frame(self.tabs, padding=14)

        self.tabs.add(
            self.book_tab,
            text='  Book a Workshop  '
        )
        self.tabs.add(
            self.my_tab,
            text='  View My Workshops  '
        )

        # Book a Workshop
        ttk.Label(
            self.book_tab,
            text='Available Workshops',
            style='Section.TLabel'
        ).pack(anchor='w')

        ttk.Label(
            self.book_tab,
            text='Select a workshop below, then click Book Selected.',
            style='Info.TLabel'
        ).pack(anchor='w', pady=(2, 12))

        table_area = ttk.Frame(self.book_tab)
        table_area.pack(fill='both', expand=True)

        columns = (
            'ID',
            'Name',
            'Location',
            'Date',
            'Time',
            'Capacity',
            'Booked',
            'Available'
        )

        self.table = ttk.Treeview(
            table_area,
            columns=columns,
            show='headings',
            selectmode='browse'
        )

        widths = (75, 190, 130, 110, 75, 75, 75, 80)

        for name, width in zip(columns, widths):
            self.table.heading(name, text=name)
            self.table.column(
                name,
                width=width,
                minwidth=60,
                anchor='w' if name == 'Name' else 'center'
            )

        self.table.tag_configure(
            'full',
            background='#FCE7E7'
        )

        bar = ttk.Scrollbar(
            table_area,
            orient='vertical',
            command=self.table.yview
        )

        self.table.configure(yscrollcommand=bar.set)

        self.table.pack(
            side='left',
            fill='both',
            expand=True
        )

        bar.pack(side='right', fill='y')

        ttk.Label(
            self.book_tab,
            text='Note: One booking per student per workshop. Full workshops cannot be booked.',
            style='Info.TLabel'
        ).pack(anchor='w', pady=(10, 5))

        buttons = ttk.Frame(self.book_tab)
        buttons.pack(fill='x', pady=8)

        ttk.Button(
            buttons,
            text='Refresh',
            command=self.refresh
        ).pack(side='left')

        ttk.Button(
            buttons,
            text='Book Selected',
            style='Book.TButton',
            command=self.book_selected
        ).pack(side='right')

        # View My Workshops
        ttk.Label(
            self.my_tab,
            text='View My Workshops',
            style='Section.TLabel'
        ).pack(anchor='w')

        ttk.Label(
            self.my_tab,
            text='Click Show to view your upcoming booked workshops.',
            style='Info.TLabel'
        ).pack(anchor='w', pady=(2, 12))

        my_area = ttk.Frame(self.my_tab)
        my_area.pack(fill='both', expand=True)

        my_columns = (
            'ID',
            'Name',
            'Location',
            'Date',
            'Time'
        )

        self.my_table = ttk.Treeview(
            my_area,
            columns=my_columns,
            show='headings'
        )

        for name, width in zip(
            my_columns,
            (90, 260, 190, 140, 110)
        ):
            self.my_table.heading(name, text=name)
            self.my_table.column(
                name,
                width=width,
                anchor='center'
            )

        my_scroll = ttk.Scrollbar(
            my_area,
            orient='vertical',
            command=self.my_table.yview
        )

        self.my_table.configure(
            yscrollcommand=my_scroll.set
        )

        self.my_table.pack(
            side='left',
            fill='both',
            expand=True
        )

        my_scroll.pack(side='right', fill='y')

        ttk.Button(
            self.my_tab,
            text='Show',
            command=self.show_my_workshops
        ).pack(anchor='e', pady=10)

        self.after(100, self.refresh)

    def refresh(self):
        try:
            workshops = get_workshops()

        except sqlite3.Error as error:
            messagebox.showerror(
                'Database Error',
                'Cannot load workshops:\n' + str(error),
                parent=self
            )
            return

        for item in self.table.get_children():
            self.table.delete(item)

        for workshop in workshops:
            workshop_id, name, location, date_time, capacity, booked = workshop

            workshop_time = datetime.fromisoformat(date_time)
            available = max(0, capacity - booked)

            self.table.insert(
                '',
                'end',
                iid=str(workshop_id),
                values=(
                    workshop_id,
                    name,
                    location,
                    workshop_time.strftime('%Y-%m-%d'),
                    workshop_time.strftime('%H:%M'),
                    capacity,
                    booked,
                    available
                ),
                tags=('full',) if available == 0 else ()
            )

    def book_selected(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                'No Selection',
                'Please select a workshop.',
                parent=self
            )
            return

        workshop_id = int(selected[0])

        if not messagebox.askyesno(
            'Confirm',
            'Book workshop ' + str(workshop_id) + '?',
            parent=self
        ):
            return

        try:
            success, message = book_workshop(
                self.student_id,
                workshop_id
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                'Database Error',
                'Booking failed:\n' + str(error),
                parent=self
            )
            return

        if success:
            messagebox.showinfo(
                'Success',
                message,
                parent=self
            )
        else:
            messagebox.showwarning(
                'Booking Unavailable',
                message,
                parent=self
            )

        self.refresh()

    def show_my_workshops(self):
        try:
            workshops = get_my_workshops(self.student_id)

        except (sqlite3.Error, ValueError) as error:
            messagebox.showerror(
                'Database Error',
                'Cannot load bookings:\n' + str(error),
                parent=self
            )
            return

        for item in self.my_table.get_children():
            self.my_table.delete(item)

        try:
            for workshop_id, name, location, date_time in workshops:
                workshop_time = datetime.fromisoformat(date_time)

                self.my_table.insert(
                    '',
                    'end',
                    values=(
                        workshop_id,
                        name,
                        location,
                        workshop_time.strftime('%Y-%m-%d'),
                        workshop_time.strftime('%H:%M')
                    )
                )

        except ValueError:
            messagebox.showerror(
                'Date Error',
                'A workshop date is invalid.',
                parent=self
            )
            return

        if not workshops:
            messagebox.showinfo(
                'My Workshops',
                'No upcoming booked workshops.',
                parent=self
            )

    def logout(self):
        if self.on_logout is not None:
            self.destroy()
            self.on_logout()
        else:
            self.winfo_toplevel().destroy()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python student_window.py STUDENT_ID')
    else:
        root = tk.Tk()
        StudentWindow(root, sys.argv[1])
        root.mainloop()