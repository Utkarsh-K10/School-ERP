# app/student_register.py

import customtkinter as ctk
from tkinter import messagebox
from models.student_controller import register_student, get_next_student_uid

class StudentRegisterWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Register New Student")
        self.master.geometry("750x750")
        self.master.configure(bg="#f5f5f5")

        self.student_uid = get_next_student_uid()
        self.entries = {}

        self.scrollable_frame = ctk.CTkScrollableFrame(self.master, width=700, height=700)
        self.scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self.scrollable_frame, text="Student Registration Form",
                    font=("Arial", 20, "bold")).pack(pady=(10, 20))

        fields = [
            ("Name", "name"),
            ("DOB (YYYY-MM-DD)", "dob"),
            ("Father's Name", "father_name"),
            ("Mother's Name", "mother_name"),
            ("Aadhar Number", "adhar_no"),
            ("Under RTE (Yes/No)", "under_rte"),
            ("APAR ID", "apar_id"),
            ("Medium (Hindi/English)", "medium"),
            ("Class", "class"),
            ("Section", "section"),
            ("Roll No", "roll_no"),
            ("Session", "session"),
            ("Address", "address"),
            ("WhatsApp No", "whatsapp_no"),
            ("Guardian Contact", "guardian_contact"),
            ("Bank Account No.", "bank_account"),
            ("IFSC Code", "ifsc_code")
        ]

        for label, key in fields:
            ctk.CTkLabel(self.scrollable_frame, text=label, anchor="w").pack(pady=(8, 0), fill="x")
            if key == "under_rte":
                combo = ctk.CTkComboBox(self.scrollable_frame, values=["Yes", "No"])
                combo.pack(pady=5)
                self.entries[key] = combo
            elif key == "medium":
                combo = ctk.CTkComboBox(self.scrollable_frame, values=["Hindi", "English"])
                combo.pack(pady=5)
                self.entries[key] = combo
            elif key == "class":
                combo = ctk.CTkComboBox(self.scrollable_frame, values=[str(i) for i in range(1, 13)])
                combo.pack(pady=5)
                combo.bind("<<ComboboxSelected>>", self.check_class)
                self.entries[key] = combo
            else:
                entry = ctk.CTkEntry(self.scrollable_frame)
                entry.pack(pady=5)
                self.entries[key] = entry

        # Subject group and school house (class 11–12 only)
        self.group_label = ctk.CTkLabel(self.scrollable_frame, text="Subject Group (11/12)")
        self.group_combo = ctk.CTkComboBox(self.scrollable_frame, values=["Maths", "Bio", "Arts", "Commerce"])

        self.house_label = ctk.CTkLabel(self.scrollable_frame, text="School House")
        self.house_combo = ctk.CTkComboBox(self.scrollable_frame, values=["Himalaya", "Satpura", "Nilgiri", "Vindhyanchal"])

        # Submit button
        ctk.CTkButton(self.scrollable_frame, text="Submit", command=self.submit_form,
                    width=200, height=40, font=("Arial", 14)).pack(pady=20)

    def check_class(self, event=None):
        class_value = self.entries['class'].get()
        if class_value in ["11", "12"]:
            self.group_label.pack(pady=(8, 0))
            self.group_combo.pack(pady=5)
            self.house_label.pack(pady=(8, 0))
            self.house_combo.pack(pady=5)
        else:
            self.group_label.pack_forget()
            self.group_combo.pack_forget()
            self.house_label.pack_forget()
            self.house_combo.pack_forget()

    def submit_form(self):
        data = {
            "student_uid": self.student_uid,
            "subject_group": self.group_combo.get() if self.entries['class'].get() in ["11", "12"] else None,
            "school_house": self.house_combo.get() if self.entries['class'].get() in ["11", "12"] else None
        }

        for key, widget in self.entries.items():
            data[key] = widget.get().strip()

        success, msg = register_student(data)
        if success:
            messagebox.showinfo("Success", msg)
            self.master.destroy()
        else:
            messagebox.showerror("Error", msg)
