# app/login.py

import customtkinter as ctk
from tkinter import messagebox
from models.user_model import verify_admin
from app.main_dashboard import MainDashboard
import os

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("School Fee System - Admin Login")
        self.master.geometry("500x400")
        self.master.resizable(False, False)

        self.frame = ctk.CTkFrame(master, corner_radius=20)
        self.frame.pack(padx=40, pady=40, expand=True, fill="both")

        # Load school logo if available
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            from PIL import Image, ImageTk
            img = ctk.CTkImage(Image.open(logo_path), size=(60, 60))
            ctk.CTkLabel(self.frame, text="", image=img).pack(pady=(10, 5))

        ctk.CTkLabel(self.frame, text="R K Memorial Hr. Sec. School", font=("Cinzel", 20, "bold")).pack(pady=(0, 20))

        ctk.CTkLabel(self.frame, text="Admin Login", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        self.username_entry = ctk.CTkEntry(self.frame, placeholder_text="Username", width=300)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*", width=300)
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self.frame, text="Login", command=self.login, width=300)
        self.login_button.pack(pady=20)

        # Theme switcher
        self.switch_mode = ctk.CTkSwitch(self.frame, text="Dark Mode", command=self.toggle_mode)
        self.switch_mode.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        if verify_admin(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.master.destroy()
            dashboard_root = ctk.CTk()
            MainDashboard(dashboard_root)
            dashboard_root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def toggle_mode(self):
        if self.switch_mode.get():
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
