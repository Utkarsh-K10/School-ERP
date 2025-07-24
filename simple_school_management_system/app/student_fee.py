# app/student_fee.py

import customtkinter as ctk
from tkinter import messagebox
from models.student_fee_controller import get_student_by_uid, add_student_fee
from models.fee_controller import get_fee_structure_by_class_section

class StudentFeeWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Fee Collection")
        self.master.geometry("600x600")

        self.student_data = None
        self.fee_structure = None

        self.main_frame = ctk.CTkFrame(master, corner_radius=20)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.main_frame, text="Fee Collection", font=("Arial", 20, "bold")).pack(pady=(10, 20))

        self.search_section()

    def search_section(self):
        search_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        search_frame.pack(pady=10)

        self.uid_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter Student UID", width=250)
        self.uid_entry.grid(row=0, column=0, padx=10)

        ctk.CTkButton(search_frame, text="Search", command=self.search_student).grid(row=0, column=1)

        self.details_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.details_frame.pack(pady=10, fill="both", expand=True)

    def search_student(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        uid = self.uid_entry.get().strip()
        if not uid:
            messagebox.showerror("Error", "Please enter a valid UID.")
            return

        self.student_data = get_student_by_uid(uid)
        if not self.student_data:
            messagebox.showerror("Error", "Student not found.")
            return

        self.fee_structure = get_fee_structure_by_class_section(
            self.student_data["class"], self.student_data["section"]
        )

        if not self.fee_structure:
            messagebox.showerror("Error", "Fee structure not found for class-section.")
            return

        # Display student name/class
        ctk.CTkLabel(self.details_frame, text=f"Name: {self.student_data['name']}", font=("Arial", 14)).pack()
        ctk.CTkLabel(self.details_frame, text=f"Class: {self.student_data['class']} - {self.student_data['section']}",
                    font=("Arial", 13)).pack(pady=5)

        self.inputs = {}
        fields = ["Discount", "Amount Received", "Late Fee", "Submission Date (YYYY-MM-DD)"]
        for field in fields:
            ctk.CTkLabel(self.details_frame, text=field).pack(pady=(10, 0))
            entry = ctk.CTkEntry(self.details_frame, width=300)
            entry.pack()
            self.inputs[field.lower().replace(" ", "_")] = entry

        # Display Total Fee
        ctk.CTkLabel(self.details_frame, text=f"Total Fee: ₹{self.fee_structure['total_fee']}",
                    font=("Arial", 13, "bold")).pack(pady=(15, 10))

        ctk.CTkButton(self.details_frame, text="Submit Fee", command=self.submit_fee,
                    fg_color="#4caf50", hover_color="#388e3c").pack(pady=20)

    def submit_fee(self):
        try:
            discount = float(self.inputs["discount"].get() or 0)
            received = float(self.inputs["amount_received"].get())
            late_fee = float(self.inputs["late_fee"].get() or 0)
            submission_date = self.inputs["submission_date_(yyyy-mm-dd)"].get().strip()

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
