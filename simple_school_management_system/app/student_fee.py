# app/student_fee.py

import tkinter as tk
from tkinter import messagebox, ttk
from models.fee_controller import get_fee_structure_by_class_section
from models.student_fee_controller import add_student_fee, get_student_by_uid

class StudentFeeWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Fee Collection")
        self.master.geometry("700x500")
        self.master.configure(bg="#f5f5f5")

        self.student_data = None
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.master, text="Fee Collection", font=("Arial", 18, "bold"), bg="#f5f5f5").pack(pady=10)

        search_frame = tk.Frame(self.master, bg="#f5f5f5")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Enter Student UID:", bg="#f5f5f5").grid(row=0, column=0, padx=5)
        self.uid_entry = tk.Entry(search_frame)
        self.uid_entry.grid(row=0, column=1, padx=5)

        tk.Button(search_frame, text="Search", command=self.search_student,
                bg="#2196f3", fg="white").grid(row=0, column=2, padx=5)

        self.details_frame = tk.Frame(self.master, bg="#f5f5f5")
        self.details_frame.pack(pady=10)

    def search_student(self):
        uid = self.uid_entry.get().strip()
        self.student_data = get_student_by_uid(uid)

        for widget in self.details_frame.winfo_children():
            widget.destroy()

        if not self.student_data:
            messagebox.showerror("Error", "Student not found.")
            return

        tk.Label(self.details_frame, text=f"Student: {self.student_data['name']}", font=("Arial", 14, "bold"), bg="#f5f5f5").pack()
        tk.Label(self.details_frame, text=f"Class: {self.student_data['class']} - {self.student_data['section']}", bg="#f5f5f5").pack()

        self.fee_structure = get_fee_structure_by_class_section(self.student_data['class'], self.student_data['section'])

        if not self.fee_structure:
            messagebox.showerror("Error", "No fee structure defined for this class-section.")
            return

        total_fee = self.fee_structure['total_fee']

        self.inputs = {}

        for i, field in enumerate(["Discount", "Received Amount", "Late Fee", "Submission Date (YYYY-MM-DD)"]):
            tk.Label(self.details_frame, text=field + ":", bg="#f5f5f5").pack(pady=3)
            entry = tk.Entry(self.details_frame)
            entry.pack(pady=3)
            self.inputs[field.lower().replace(" ", "_")] = entry

        tk.Label(self.details_frame, text=f"Total Fee: ₹{total_fee}", font=("Arial", 12, "bold"), bg="#f5f5f5").pack(pady=5)

        tk.Button(self.details_frame, text="Submit Fee", command=self.submit_fee,
                bg="#4caf50", fg="white").pack(pady=10)

    def submit_fee(self):
        try:
            discount = float(self.inputs["discount"].get() or 0)
            received = float(self.inputs["received_amount"].get())
            late_fee = float(self.inputs["late_fee"].get() or 0)
            submission_date = self.inputs["submission_date_(yyyy-mm-dd)"].get()

            total_fee = self.fee_structure["total_fee"]
            outstanding = total_fee - discount - received + late_fee

            data = {
                "student_uid": self.student_data["student_uid"],
                "total_fee": total_fee,
                "discount": discount,
                "received": received,
                "outstanding": outstanding,
                "late_fee": late_fee,
                "submission_date": submission_date
            }

            success, msg = add_student_fee(data)
            if success:
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
