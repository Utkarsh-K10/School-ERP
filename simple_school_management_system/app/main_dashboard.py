# app/main_dashboard.py

import customtkinter as ctk
from models.dashboard_model import get_stats
from app.student_register import StudentRegisterWindow
from app.fee_management import FeeStructureWindow
from app.student_fee import StudentFeeWindow
from app.receipt_generator import ReceiptWindow
from app.bulk_import import BulkUploadWindow
from app.id_card_generator import IDCardWindow
from app.bulk_id_export import BulkIDCardExporter
import os
from PIL import Image

class MainDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard - School Fee System")
        self.root.geometry("950x700")
        self.root.minsize(800, 600)
        self.frame = ctk.CTkFrame(self.root, corner_radius=20)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.setup_ui()

    def setup_ui(self):
        header = ctk.CTkFrame(self.frame, fg_color="transparent")
        header.pack(fill="x", pady=(10, 30))

        # School logo
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            img = ctk.CTkImage(Image.open(logo_path), size=(60, 60))
            ctk.CTkLabel(header, image=img, text="").pack(side="left", padx=20)

        # School name and address
        text_frame = ctk.CTkFrame(header, fg_color="transparent")
        text_frame.pack(side="left")

        ctk.CTkLabel(text_frame, text="R K Memorial Hr. Sec. School", font=("Cinzel", 22, "bold")).pack(anchor="w")
        ctk.CTkLabel(text_frame, text="Hanuman Nagar, Ward-17, Satna (M.P.)", font=("Arial", 14)).pack(anchor="w")

        # Load stats
        stats = get_stats()
        stat_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        stat_frame.pack(pady=10)

        self.create_stat_card(stat_frame, "Total Students", stats["total_students"], "#2196f3", 0)
        self.create_stat_card(stat_frame, "Fees Collected", f"₹{stats['total_collected']}", "#4caf50", 1)
        self.create_stat_card(stat_frame, "Outstanding Fees", f"₹{stats['total_outstanding']}", "#f44336", 2)

        # Navigation buttons
        nav_frame = ctk.CTkFrame(self.frame)
        nav_frame.pack(pady=30)

        buttons = [
            ("➕ Register Student", self.open_register_student),
            ("💰 Fee Management", self.open_fee_management),
            ("📥 Bulk Upload", self.open_bulk_upload),
            ("🧾 Generate Receipt", self.open_receipt_generator),
            ("🪪 Generate ID Card", self.open_id_generator),
            ("🔓 Logout", self.logout),
        ]

        for text, command in buttons:
            ctk.CTkButton(nav_frame, text=text, command=command, font=("Arial", 14),
                        width=300, height=40).pack(pady=10)

    def create_stat_card(self, parent, title, value, color, column):
        card = ctk.CTkFrame(parent, width=250, height=100, corner_radius=15, fg_color=color)
        card.grid(row=0, column=column, padx=15, pady=15)
        card.grid_propagate(False)

        ctk.CTkLabel(card, text=title, font=("Arial", 13, "bold"), text_color="white").pack(pady=(15, 5))
        ctk.CTkLabel(card, text=str(value), font=("Arial", 20, "bold"), text_color="white").pack()

    def open_register_student(self):
        win = ctk.CTkToplevel(self.root)
        StudentRegisterWindow(win)

    def open_fee_management(self):
        win = ctk.CTkToplevel(self.root)
        FeeStructureWindow(win)

    def open_bulk_upload(self):
        win = ctk.CTkToplevel(self.root)
        BulkUploadWindow(win)

    def open_receipt_generator(self):
        win = ctk.CTkToplevel(self.root)
        ReceiptWindow(win)

    def open_id_generator(self):
        win = ctk.CTkToplevel(self.root)
        IDCardWindow(win)


    def open_bulk_id_export(self):
        win = ctk.CTkToplevel(self.root)
        BulkIDCardExporter(win)


    def logout(self):
        self.root.destroy()
        import main
        main.main()
