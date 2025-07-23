# app/bulk_import.py

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from models.student_controller import register_student, get_next_student_uid

class BulkUploadWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Bulk Upload Students")
        self.master.geometry("600x300")
        self.master.configure(bg="#f5f5f5")

        tk.Label(self.master, text="Bulk Upload from Excel", font=("Arial", 18, "bold"),
                 bg="#f5f5f5", fg="#003366").pack(pady=20)

        tk.Button(self.master, text="Select Excel File", command=self.select_file,
                  bg="#2196f3", fg="white", font=("Arial", 12)).pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
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
                    print(f"Error in row: {e}")
                    fail_count += 1

            messagebox.showinfo("Upload Complete",
                                f"Success: {success_count} students\nFailed: {fail_count}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to read Excel file.\n{e}")
