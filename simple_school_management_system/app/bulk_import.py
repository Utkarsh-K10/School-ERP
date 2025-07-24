# app/bulk_import.py

import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
from models.student_controller import register_student, get_next_student_uid

class BulkUploadWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Bulk Upload Students")
        self.master.geometry("600x400")

        self.frame = ctk.CTkFrame(master, corner_radius=20)
        self.frame.pack(padx=30, pady=30, fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="Bulk Upload from Excel",
                    font=("Arial", 20, "bold")).pack(pady=(10, 30))

        ctk.CTkButton(self.frame, text="Select Excel File",
                    command=self.select_file, width=250).pack(pady=20)

        self.result_label = ctk.CTkLabel(self.frame, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx")]
        )
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)
            success_count = 0
            fail_count = 0

            for _, row in df.iterrows():
                try:
                    student_uid = get_next_student_uid()

                    data = {
                        "student_uid": student_uid,
                        "name": str(row["name"]),
                        "dob": str(row["dob"]),
                        "father_name": str(row["father_name"]),
                        "mother_name": str(row["mother_name"]),
                        "class": str(row["class"]),
                        "section": str(row["section"]),
                        "roll_no": str(row["roll_no"]),
                        "adhar_no": str(row["adhar_no"]),
                        "under_rte": str(row["under_rte"]).strip().lower() == "yes",
                        "apar_id": str(row["apar_id"]),
                        "medium": str(row["medium"]),
                        "session": str(row["session"]),
                        "address": str(row["address"]),
                        "whatsapp_no": str(row["whatsapp_no"]),
                        "guardian_contact": str(row["guardian_contact"]),
                        "bank_account": str(row["bank_account"]),
                        "ifsc_code": str(row["ifsc_code"]),
                        "subject_group": str(row.get("subject_group")) if str(row["class"]) in ["11", "12"] else None,
                        "school_house": str(row.get("school_house")) if str(row["class"]) in ["11", "12"] else None,
                    }

                    success, _ = register_student(data)
                    if success:
                        success_count += 1
                    else:
                        fail_count += 1
                except Exception as e:
                    print(f"Row error: {e}")
                    fail_count += 1

            self.result_label.configure(
                text=f"✅ Uploaded: {success_count}  |  ❌ Failed: {fail_count}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Could not read Excel file:\n{e}")
