# app/receipt_generator.py

import tkinter as tk
from tkinter import messagebox
from models.student_fee_controller import get_student_by_uid, get_latest_fee_record
from PIL import Image, ImageTk
import os
from fpdf import FPDF
import datetime

class ReceiptWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Generate Fee Receipt")
        self.master.geometry("700x600")
        self.master.configure(bg="#f5f5f5")

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.master, text="Generate Fee Receipt", font=("Arial", 18, "bold"),
                 bg="#f5f5f5", fg="#003366").pack(pady=10)

        form = tk.Frame(self.master, bg="#f5f5f5")
        form.pack(pady=10)

        tk.Label(form, text="Enter Student UID:", bg="#f5f5f5").grid(row=0, column=0, pady=10)
        self.uid_entry = tk.Entry(form, width=30)
        self.uid_entry.grid(row=0, column=1, padx=10)

        tk.Button(form, text="Search", command=self.generate_receipt_view,
                  bg="#2196f3", fg="white").grid(row=0, column=2, padx=5)

        self.result_frame = tk.Frame(self.master, bg="#ffffff", relief="sunken", borderwidth=1)
        self.result_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    def generate_receipt_view(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        uid = self.uid_entry.get().strip()
        student = get_student_by_uid(uid)
        fee = get_latest_fee_record(uid)

        if not student or not fee:
            messagebox.showerror("Error", "Student or Fee data not found.")
            return

        # School Header
        logo_path = os.path.join("assets", "logo.png")
        try:
            logo_img = Image.open(logo_path).resize((60, 60))
            logo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(self.result_frame, image=logo, bg="white")
            logo_label.image = logo
            logo_label.pack(pady=5)
        except:
            pass

        tk.Label(self.result_frame, text="R K Memorial Hr. Sec. School", font=("Cinzel", 18, "bold"),
                 bg="white", fg="#000000").pack()
        tk.Label(self.result_frame, text="Hanuman Nagar, Ward 17, Satna (M.P.)", bg="white",
                 font=("Arial", 12)).pack()
        tk.Label(self.result_frame, text="Fee Receipt", font=("Arial", 14, "bold"), bg="white", pady=10).pack()

        details = [
            f"Student UID: {student['student_uid']}",
            f"Name: {student['name']}",
            f"Class: {student['class']} - {student['section']}",
            f"Date of Payment: {fee['submission_date']}",
            f"Total Fee: ₹{fee['total_fee']}",
            f"Discount: ₹{fee['discount']}",
            f"Late Fee: ₹{fee['late_fee']}",
            f"Amount Received: ₹{fee['received']}",
            f"Outstanding: ₹{fee['outstanding']}",
        ]

        for d in details:
            tk.Label(self.result_frame, text=d, font=("Arial", 11), bg="white").pack(anchor="w", padx=20)

        tk.Button(self.result_frame, text="Print / Save PDF", command=lambda: self.export_pdf(student, fee),
                bg="#4caf50", fg="white", font=("Arial", 12)).pack(pady=20)

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
            pdf.cell(50, 8, f"{label}:", 0)
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
        messagebox.showinfo("PDF Saved", f"Receipt saved as {filename}")
