# app/receipt_generator.py

import customtkinter as ctk
from tkinter import messagebox
from models.student_fee_controller import get_student_by_uid, get_latest_fee_record
from PIL import Image
import os
from fpdf import FPDF

class ReceiptWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Fee Receipt Generator")
        self.master.geometry("700x600")

        self.frame = ctk.CTkFrame(master, corner_radius=20)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="Generate Fee Receipt", font=("Arial", 20, "bold")).pack(pady=(10, 20))

        self.uid_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Student UID", width=300)
        self.uid_entry.pack(pady=10)

        ctk.CTkButton(self.frame, text="Search", command=self.load_receipt).pack()

        self.result_frame = ctk.CTkFrame(self.frame, corner_radius=15, fg_color="#ffffff")
        self.result_frame.pack(pady=30, fill="both", expand=True)

    def load_receipt(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        uid = self.uid_entry.get().strip()
        student = get_student_by_uid(uid)
        fee = get_latest_fee_record(uid)

        if not student or not fee:
            messagebox.showerror("Error", "Student or latest fee record not found.")
            return

        # School branding
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            logo_img = ctk.CTkImage(Image.open(logo_path), size=(60, 60))
            ctk.CTkLabel(self.result_frame, text="", image=logo_img).pack(pady=(10, 5))

        ctk.CTkLabel(self.result_frame, text="R K Memorial Hr. Sec. School",
                    font=("Cinzel", 18, "bold"), text_color="#000").pack()
        ctk.CTkLabel(self.result_frame, text="Hanuman Nagar, Ward 17, Satna (M.P.)",
                    font=("Arial", 13)).pack(pady=(0, 10))

        ctk.CTkLabel(self.result_frame, text="FEE RECEIPT", font=("Arial", 14, "bold")).pack(pady=10)

        detail_fields = [
            ("Student UID", student["student_uid"]),
            ("Name", student["name"]),
            ("Class", f"{student['class']} - {student['section']}"),
            ("Date of Payment", fee["submission_date"]),
            ("Total Fee", f"₹{fee['total_fee']}"),
            ("Discount", f"₹{fee['discount']}"),
            ("Late Fee", f"₹{fee['late_fee']}"),
            ("Amount Received", f"₹{fee['received']}"),
            ("Outstanding", f"₹{fee['outstanding']}")
        ]

        for label, value in detail_fields:
            ctk.CTkLabel(self.result_frame, text=f"{label}: {value}",
                        font=("Arial", 12), anchor="w", justify="left").pack(padx=30, anchor="w")

        ctk.CTkButton(self.result_frame, text="Save as PDF", command=lambda: self.export_pdf(student, fee),
                    fg_color="#4caf50", hover_color="#388e3c", width=200).pack(pady=20)

    def export_pdf(self, student, fee):
        filename = f"Receipt_{student['student_uid']}.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "R K Memorial Hr. Sec. School", ln=True, align='C')
        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, "Hanuman Nagar, Ward 17, Satna (M.P.)", ln=True, align='C')
        pdf.cell(200, 10, "FEE RECEIPT", ln=True, align='C')
        pdf.ln(10)

        def write(label, value):
            pdf.set_font("Arial", "B", 11)
            pdf.cell(60, 8, f"{label}:", 0)
            pdf.set_font("Arial", "", 11)
            pdf.cell(100, 8, f"{value}", ln=True)

        write("Student UID", student['student_uid'])
        write("Name", student['name'])
        write("Class", f"{student['class']} - {student['section']}")
        write("Date of Payment", str(fee['submission_date']))
        write("Total Fee", f"₹{fee['total_fee']}")
        write("Discount", f"₹{fee['discount']}")
        write("Late Fee", f"₹{fee['late_fee']}")
        write("Amount Received", f"₹{fee['received']}")
        write("Outstanding", f"₹{fee['outstanding']}")

        pdf.ln(10)
        pdf.cell(200, 8, "Thank you for your payment.", ln=True, align='C')

        pdf.output(filename)
        messagebox.showinfo("Saved", f"Receipt saved as {filename}")
