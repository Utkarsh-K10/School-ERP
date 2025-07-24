# app/bulk_id_export.py

import os
import qrcode
from fpdf import FPDF
from PIL import Image
from tkinter import messagebox
import customtkinter as ctk
from models.student_fee_controller import get_all_students

class BulkIDCardExporter:
    def __init__(self, master):
        self.master = master
        self.master.title("Bulk ID Card Export")
        self.master.geometry("500x300")

        self.frame = ctk.CTkFrame(master, corner_radius=20)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="Bulk Export Student ID Cards",
                     font=("Arial", 20, "bold")).pack(pady=30)

        ctk.CTkButton(self.frame, text="Generate All IDs", command=self.export_bulk_ids,
                      width=250).pack(pady=20)

    def export_bulk_ids(self):
        students = get_all_students()

        if not students:
            messagebox.showwarning("No Data", "No student records found.")
            return

        try:
            self.generate_pdf(students)
            messagebox.showinfo("Success", "All ID cards exported to bulk_student_ids.pdf")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate ID cards:\n{e}")

    def generate_pdf(self, students):
        logo_path = os.path.join("assets", "logo.png")
        default_img = os.path.join("assets", "default_photo.png")

        # A8 dimensions in points
        width_pt = 74 * 2.83
        height_pt = 52 * 2.83

        pdf = FPDF("P", "pt", [width_pt, height_pt])

        for student in students:
            image_path = student.get("image_path") or default_img

            # Generate QR
            qr_path = f"temp_qr_{student['student_uid']}.png"
            qrcode.make(student["student_uid"]).save(qr_path)

            pdf.add_page()

            # Logo
            if os.path.exists(logo_path):
                pdf.image(logo_path, x=10, y=10, w=40)

            # Header
            pdf.set_font("Arial", "B", 11)
            pdf.set_xy(55, 10)
            pdf.multi_cell(120, 10, "R K Memorial Hr. Sec. School\nHanuman Nagar, Satna (M.P.)", align="L")

            # Photo
            if os.path.exists(image_path):
                pdf.image(image_path, x=10, y=40, w=35, h=45)

            # Info
            pdf.set_xy(50, 45)
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 12, f"ID: {student['student_uid']}", ln=True)
            pdf.cell(0, 12, f"Father: {student['father_name']}", ln=True)
            pdf.cell(0, 12, f"Contact: {student['guardian_contact']}", ln=True)

            # QR Code
            pdf.image(qr_path, x=135, y=40, w=35, h=35)
            os.remove(qr_path)

        pdf.output("bulk_student_ids.pdf")
