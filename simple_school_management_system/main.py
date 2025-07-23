# Entry point - main.py

import tkinter as tk
from app.login import LoginWindow
from config.db_config import initialize_database

def main():
    initialize_database()
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
