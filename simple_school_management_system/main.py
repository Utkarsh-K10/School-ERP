# Entry point - main.py

import sys
sys.path.append('../')
import customtkinter as ctk
from app.login import LoginWindow
from models.init_db import initialize_db

def main():
    initialize_db()

    ctk.set_appearance_mode("System")  # Options: "Light", "Dark", "System"
    ctk.set_default_color_theme("blue")  # You can also try "green", "dark-blue"

    root = ctk.CTk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
