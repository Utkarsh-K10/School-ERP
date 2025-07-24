# app/fee_management.py

import customtkinter as ctk
from tkinter import ttk, messagebox
from models.fee_controller import get_all_fee_structures, add_fee_structure, delete_fee_structure

class FeeStructureWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Class-wise Fee Structure")
        self.master.geometry("900x650")

        self.inputs = {}

        self.container = ctk.CTkFrame(master, corner_radius=15)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(self.container, text="Fee Structure Management",
                    font=("Arial", 20, "bold")).pack(pady=(10, 20))

        self.setup_form()
        self.setup_table()
        self.load_fee_data()

    def setup_form(self):
        form_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        form_frame.pack(pady=10)

        field_list = [
            ("Class", "class"),
            ("Section", "section"),
            ("Tuition Fee", "tuition_fee"),
            ("Transport Fee", "transport_fee"),
            ("Activity Fee", "activity_fee"),
            ("Admission Fee", "admission_fee")
        ]

        for i, (label, key) in enumerate(field_list):
            ctk.CTkLabel(form_frame, text=label).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = ctk.CTkEntry(form_frame, width=200)
            entry.grid(row=i, column=1, pady=5)
            self.inputs[key] = entry

        ctk.CTkButton(form_frame, text="Add Fee Structure", command=self.add_structure,
                    width=200, height=35).grid(row=len(field_list), columnspan=2, pady=15)

    def setup_table(self):
        table_frame = ctk.CTkFrame(self.container)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=30)

        self.tree = ttk.Treeview(table_frame, columns=("class", "section", "tuition", "transport", "activity", "admission", "total"), show="headings")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkButton(self.container, text="Delete Selected", command=self.delete_selected,
                      fg_color="#f44336", hover_color="#d32f2f", width=160).pack(pady=10)

    def load_fee_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in get_all_fee_structures():
            self.tree.insert("", "end", values=row)

    def add_structure(self):
        try:
            data = {k: self.inputs[k].get().strip() for k in self.inputs}
            fees = [float(data["tuition_fee"]), float(data["transport_fee"]),
                    float(data["activity_fee"]), float(data["admission_fee"])]
            total = sum(fees)

            add_fee_structure(data["class"], data["section"], *fees, total)
            self.load_fee_data()
            messagebox.showinfo("Success", "Fee structure added.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values.")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0])["values"]
        if messagebox.askyesno("Confirm", f"Delete fee structure for class {values[0]}-{values[1]}?"):
            delete_fee_structure(values[0], values[1])
            self.load_fee_data()
