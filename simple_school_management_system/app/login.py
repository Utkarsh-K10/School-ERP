# app/login.py

import tkinter as tk
from tkinter import messagebox
from models.user_model import verify_admin
from app.main_dashboard import MainDashboard

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("School Fee System - Login")
        self.master.geometry("400x250")
        self.master.resizable(False, False)

        self.frame = tk.Frame(master, bg="#f0f0f0")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Admin Login", font=("Cinzel", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        tk.Label(self.frame, text="Username:", bg="#f0f0f0").pack(pady=(10, 0))
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack(pady=5)

        tk.Label(self.frame, text="Password:", bg="#f0f0f0").pack(pady=(10, 0))
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.frame, text="Login", command=self.login, bg="#007acc", fg="white", width=15)
        self.login_button.pack(pady=15)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        if verify_admin(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.master.destroy()
            root = tk.Tk()
            MainDashboard(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials.")
