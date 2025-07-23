# app/main_dashboard.py

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from models.dashboard_model import get_stats
from app.student_register import StudentRegisterWindow

class MainDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard - School Fee System")
        self.root.geometry("900x600")
        self.root.configure(bg="#e8f0fe")

        self.setup_ui()

    def setup_ui(self):
        # Top banner
        banner = tk.Frame(self.root, bg="#003366", height=100)
        banner.pack(fill=tk.X)

        # School Logo
        logo_path = os.path.join("assets", "logo.png")
        logo_img = Image.open(logo_path).resize((80, 80))
        logo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(banner, image=logo, bg="#003366")
        logo_label.image = logo  # Keep reference
        logo_label.pack(side=tk.LEFT, padx=20, pady=10)

        # School Name and Address
        title_frame = tk.Frame(banner, bg="#003366")
        title_frame.pack(side=tk.LEFT)

        tk.Label(title_frame, text="R K Memorial Hr. Sec. School", fg="white",
                font=("Cinzel", 22, "bold"), bg="#003366").pack(anchor="w")
        tk.Label(title_frame, text="Hanuman Nagar, Ward-17, Satna (M.P.)", fg="white",
                font=("Arial", 12), bg="#003366").pack(anchor="w")

        # Stats
        stats = get_stats()
        content = tk.Frame(self.root, bg="#e8f0fe")
        content.pack(fill=tk.BOTH, expand=True, pady=20)

        self.create_stat_card(content, "Total Students", stats['total_students'], "#4caf50", 0)
        self.create_stat_card(content, "Total Fees Collected", f"₹{stats['total_collected']}", "#2196f3", 1)
        self.create_stat_card(content, "Outstanding Fees", f"₹{stats['total_outstanding']}", "#f44336", 2)

        # Navigation Buttons
        nav_frame = tk.Frame(self.root, bg="#e8f0fe")
        nav_frame.pack(pady=30)

        buttons = [
            ("➕ Register Student", self.open_register_student),
            ("💰 Fee Management", self.open_fee_management),
            ("📥 Bulk Upload (Excel)", self.open_bulk_upload),
            ("🧾 Generate Receipt", self.open_receipt_generator),
            ("🔓 Logout", self.logout),
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(nav_frame, text=text, command=command,
                    width=30, height=2, bg="#007acc", fg="white",
                    font=("Arial", 11, "bold")).grid(row=i, column=0, pady=10)

    def create_stat_card(self, parent, title, value, bg_color, column):
        frame = tk.Frame(parent, bg=bg_color, width=250, height=100)
        frame.grid(row=0, column=column, padx=30)
        frame.grid_propagate(False)

        tk.Label(frame, text=title, font=("Arial", 12, "bold"), fg="white", bg=bg_color).pack(pady=(15, 5))
        tk.Label(frame, text=value, font=("Arial", 18, "bold"), fg="white", bg=bg_color).pack()

    def open_register_student(self):
        win = tk.Toplevel(self.root)
        StudentRegisterWindow(win)

    def open_fee_management(self):
        print("Coming soon...")

    def open_bulk_upload(self):
        print("Coming soon...")

    def open_receipt_generator(self):
        print("Coming soon...")

    def logout(self):
        self.root.destroy()
        import main
        main.main()
