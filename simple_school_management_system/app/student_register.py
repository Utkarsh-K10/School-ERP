# app/student_register.py

import tkinter as tk
from tkinter import messagebox, ttk
from models.student_controller import register_student, get_next_student_uid

class StudentRegisterWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Register New Student")
        self.master.geometry("700x750")
        self.master.configure(bg="#f5f5f5")

        self.student_uid = get_next_student_uid()
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.master, text="Student Registration Form", font=("Arial", 18, "bold"),
                bg="#f5f5f5", fg="#003366").pack(pady=15)

        form = tk.Frame(self.master, bg="#f5f5f5")
        form.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.entries = {}

        fields = [
            ("Name", "name"),
            ("Date of Birth (YYYY-MM-DD)", "dob"),
            ("Father's Name", "father_name"),
            ("Mother's Name", "mother_name"),
            ("Aadhar Number", "adhar_no"),
            ("Under RTE", "under_rte"),
            ("APAR ID", "apar_id"),
            ("Medium", "medium"),
            ("Class", "class"),
            ("Section", "section"),
            ("Roll No", "roll_no"),
            ("Session", "session"),
            ("Address", "address"),
            ("WhatsApp No", "whatsapp_no"),
            ("Guardian Contact", "guardian_contact"),
            ("Bank A/C No", "bank_account"),
            ("IFSC Code", "ifsc_code")
        ]

        for idx, (label, key) in enumerate(fields):
            tk.Label(form, text=label, bg="#f5f5f5").grid(row=idx, column=0, sticky="w", pady=5)
            entry = tk.Entry(form, width=40)
            entry.grid(row=idx, column=1, pady=5, padx=5)
            self.entries[key] = entry

        # Dropdowns
        self.entries['under_rte'] = ttk.Combobox(form, values=["Yes", "No"], state="readonly")
        self.entries['under_rte'].grid(row=5, column=1, pady=5, padx=5)

        self.entries['medium'] = ttk.Combobox(form, values=["Hindi", "English"], state="readonly")
        self.entries['medium'].grid(row=7, column=1, pady=5, padx=5)

        self.entries['class'] = ttk.Combobox(form, values=[str(c) for c in range(1, 13)], state="readonly")
        self.entries['class'].grid(row=8, column=1, pady=5, padx=5)
        self.entries['class'].bind("<<ComboboxSelected>>", self.check_class_fields)

        # Optional fields: Subject Group & School House (for class 11/12)
        self.subject_group_var = tk.StringVar()
        self.school_house_var = tk.StringVar()

        self.group_label = tk.Label(form, text="Subject Group", bg="#f5f5f5")
        self.group_combo = ttk.Combobox(form, textvariable=self.subject_group_var,
                                        values=["Maths", "Bio", "Arts", "Commerce"], state="readonly")

        self.house_label = tk.Label(form, text="School House", bg="#f5f5f5")
        self.house_combo = ttk.Combobox(form, textvariable=self.school_house_var,
                                        values=["Himalaya", "Satpura", "Nilgiri", "Vindhyanchal"], state="readonly")

        # Submit button
        tk.Button(self.master, text="Submit", command=self.submit_form, bg="#4caf50", fg="white",
                font=("Arial", 12, "bold")).pack(pady=20)

    def check_class_fields(self, event=None):
        selected_class = self.entries['class'].get()
        if selected_class in ["11", "12"]:
            self.group_label.grid(row=17, column=0, sticky="w", pady=5)
            self.group_combo.grid(row=17, column=1, pady=5, padx=5)
            self.house_label.grid(row=18, column=0, sticky="w", pady=5)
            self.house_combo.grid(row=18, column=1, pady=5, padx=5)
        else:
            self.group_label.grid_forget()
            self.group_combo.grid_forget()
            self.house_label.grid_forget()
            self.house_combo.grid_forget()

    def submit_form(self):
        data = {
            "student_uid": self.student_uid,
            "subject_group": self.subject_group_var.get() if self.entries['class'].get() in ["11", "12"] else None,
            "school_house": self.school_house_var.get() if self.entries['class'].get() in ["11", "12"] else None
        }

        for key, entry in self.entries.items():
            data[key] = entry.get()

        success, msg = register_student(data)
        if success:
            messagebox.showinfo("Success", msg)
            self.master.destroy()
        else:
            messagebox.showerror("Error", msg)
