# app/id_card_generator.py

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageDraw
from fpdf import FPDF
import qrcode
import os

from models.student_fee_controller import get_student_by_uid

class IDCardWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Generate Student ID Card")
        self.master.geometry("600x400")

        self.frame = ctk.CTkFrame(master, corner_radius=20)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.frame, text="Generate ID Card", font=("Arial", 20, "bold")).pack(pady=20)

        self.uid_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Student UID", width=300)
        self.uid_entry.pack(pady=10)

        ctk.CTkButton(self.frame, text="Generate ID", command=self.generate_id_card).pack(pady=10)

    def generate_id_card(self):
        uid = self.uid_entry.get().strip()
        if not uid:
            messagebox.showerror("Error", "Please enter a valid UID.")
            return

        student = get_student_by_uid(uid)
        if not student:
            messagebox.showerror("Error", "Student not found.")
            return

        self.preview_id_card(student)
    
    def preview_id_card(self, student):
        preview_win = ctk.CTkToplevel(self.master)
        preview_win.title("ID Card Preview")
        preview_win.geometry("260x190")

        canvas = ctk.CTkCanvas(preview_win, width=220, height=150, bg="white", highlightthickness=1, highlightbackground="black")
        canvas.pack(pady=10)

        # School Logo
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).resize((30, 30))
            logo_img = ImageTk.PhotoImage(logo)
            canvas.create_image(20, 20, anchor="nw", image=logo_img)
            canvas.logo_img = logo_img

        # Header Text
        canvas.create_text(60, 20, anchor="nw", text="R K Memorial Hr. Sec. School", font=("Arial", 8, "bold"))
        canvas.create_text(60, 34, anchor="nw", text="Hanuman Nagar, Satna (M.P.)", font=("Arial", 7))

        # Student Image
        student_img_path = student.get("image_path") or "assets/default_photo.png"
        if os.path.exists(student_img_path):
            photo = Image.open(student_img_path).resize((45, 50))
            photo_img = ImageTk.PhotoImage(photo)
            canvas.create_image(15, 60, anchor="nw", image=photo_img)
            canvas.photo_img = photo_img

        # Student Info
        canvas.create_text(70, 65, anchor="nw", text=f"ID: {student['student_uid']}", font=("Arial", 7))
        canvas.create_text(70, 78, anchor="nw", text=f"Father: {student['father_name']}", font=("Arial", 7))
        canvas.create_text(70, 91, anchor="nw", text=f"Contact: {student['guardian_contact']}", font=("Arial", 7))

        # QR Code
        qr_img = qrcode.make(student['student_uid'])
        qr_path = f"temp_qr_{student['student_uid']}.png"
        qr_img.save(qr_path)
        qr = Image.open(qr_path).resize((35, 35))
        qr_tk = ImageTk.PhotoImage(qr)
        canvas.create_image(170, 100, anchor="nw", image=qr_tk)
        canvas.qr_tk = qr_tk

        # Save Button
        ctk.CTkButton(preview_win, text="Save as PDF", command=lambda: [self.export_id_pdf(student), preview_win.destroy()]).pack(pady=5)

        preview_win.resizable(False, False)


    def export_id_pdf(self, student):
        # File settings
        filename = f"ID_{student['student_uid']}.pdf"
        logo_path = os.path.join("assets", "logo.png")
        image_path = student.get("image_path") or "assets/default_photo.png"

        # Prepare QR Code
        qr = qrcode.make(student['student_uid'])
        qr_path = f"temp_qr_{student['student_uid']}.png"
        qr.save(qr_path)

        # PDF A8 size in mm (74x52 mm) => convert to pt (1mm = ~2.83 pt)
        width_pt = 74 * 2.83
        height_pt = 52 * 2.83

        pdf = FPDF("P", "pt", [width_pt, height_pt])
        pdf.add_page()
        pdf.set_auto_page_break(False)

        # School Logo
        if os.path.exists(logo_path):
            pdf.image(logo_path, x=10, y=10, w=40)

        # School Name
        pdf.set_font("Arial", "B", 11)
        pdf.set_xy(55, 10)
        pdf.multi_cell(120, 10, "R K Memorial Hr. Sec. School\nHanuman Nagar, Satna (M.P.)", align="L")

        # Photo
        if os.path.exists(image_path):
            pdf.image(image_path, x=10, y=40, w=35, h=45)

        # Student Info
        pdf.set_xy(50, 45)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 12, f"ID: {student['student_uid']}", ln=True)
        pdf.cell(0, 12, f"Father: {student['father_name']}", ln=True)
        pdf.cell(0, 12, f"Contact: {student['guardian_contact']}", ln=True)

        # QR Code
        pdf.image(qr_path, x=135, y=40, w=35, h=35)

        # Clean up temp QR
        os.remove(qr_path)

        # Save
        pdf.output(filename)
