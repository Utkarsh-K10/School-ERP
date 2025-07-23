# app/fee_management.py

import tkinter as tk
from tkinter import ttk, messagebox
from models.fee_controller import get_all_fee_structures, add_fee_structure, delete_fee_structure
from app.fee_management import FeeStructureWindow

class FeeStructureWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Class-wise Fee Structure")
        self.master.geometry("900x600")
        self.master.configure(bg="#f5f5f5")

        tk.Label(self.master, text="Fee Structure Management", font=("Arial", 18, "bold"),
                bg="#f5f5f5", fg="#003366").pack(pady=10)

        self.setup_form()
        self.setup_table()
        self.load_fee_data()

    def setup_form(self):
        form = tk.Frame(self.master, bg="#f5f5f5")
        form.pack(pady=10)

        self.inputs = {}

        labels = [
            ("Class", "class"),
            ("Section", "section"),
            ("Tuition Fee", "tuition_fee"),
            ("Transport Fee", "transport_fee"),
            ("Activity Fee", "activity_fee"),
            ("Admission Fee", "admission_fee")
        ]

        for i, (label, key) in enumerate(labels):
            tk.Label(form, text=label, bg="#f5f5f5").grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(form)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.inputs[key] = entry

        tk.Button(form, text="Add Fee Structure", command=self.add_structure,
                bg="#4caf50", fg="white").grid(row=len(labels), columnspan=2, pady=10)

    def setup_table(self):
        columns = ("class", "section", "tuition", "transport", "activity", "admission", "total")

        self.tree = ttk.Treeview(self.master, columns=columns, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=100)

        self.tree.bind("<Double-1>", self.on_row_double_click)

        tk.Button(self.master, text="Delete Selected", command=self.delete_selected,
                bg="#f44336", fg="white").pack(pady=5)

    def load_fee_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in get_all_fee_structures():
            self.tree.insert("", "end", values=row)

    def add_structure(self):
        try:
            data = {k: self.inputs[k].get() for k in self.inputs}
            fees = [float(data["tuition_fee"]), float(data["transport_fee"]),
                    float(data["activity_fee"]), float(data["admission_fee"])]
            total = sum(fees)
            add_fee_structure(data["class"], data["section"], *fees, total)
            self.load_fee_data()
            messagebox.showinfo("Success", "Fee structure added.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    def open_fee_management(self):
        win = tk.Toplevel(self.root)
        FeeStructureWindow(win)

    
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0])["values"]
        if messagebox.askyesno("Confirm", f"Delete fee structure for class {values[0]}-{values[1]}?"):
            delete_fee_structure(values[0], values[1])
            self.load_fee_data()

    def on_row_double_click(self, event):
        messagebox.showinfo("Edit", "Edit feature coming soon!")
