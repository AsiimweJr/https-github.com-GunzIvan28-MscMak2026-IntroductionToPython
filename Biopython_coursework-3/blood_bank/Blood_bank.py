"""
Simple Blood Donor Registry with a Search Bar
----------------------------------------------
Run with: python blood_donor_registry.py
Requires: pip install matplotlib
"""

import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter

# --- Setup matplotlib to work inside tkinter window ---
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


class BloodDonorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Donor Registry")
        self.root.geometry("1000x650")

        # Basic list to hold all our donor data
        self.donors = []

        # Create different layout frames
        self.build_form()
        self.build_table()
        self.build_chart()

        # Show empty chart at the start
        self.refresh_chart()

    # ==========================================
    # 1) THE ENTRY FORM
    # ==========================================
    def build_form(self):
        form = ttk.LabelFrame(self.root, text="Add New Donor", padding=10)
        form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Variables linked to what the user types
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.group_var = tk.StringVar()
        self.contact_var = tk.StringVar()

        # Name field
        ttk.Label(form, text="Donor Name:").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.name_var, width=25).grid(row=0, column=1, pady=4)

        # Age field
        ttk.Label(form, text="Age:").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.age_var, width=25).grid(row=1, column=1, pady=4)

        # Blood group dropdown
        ttk.Label(form, text="Blood Group:").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Combobox(form, textvariable=self.group_var, values=BLOOD_GROUPS, state="readonly", width=22).grid(row=2, column=1, pady=4)

        # Contact info field
        ttk.Label(form, text="Contact Info:").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.contact_var, width=25).grid(row=3, column=1, pady=4)

        # Submit button
        ttk.Button(form, text="Submit Donor", command=self.add_donor).grid(row=4, column=0, columnspan=2, pady=12)

    # ==========================================
    # 2) THE TABLE & SEARCH BAR
    # ==========================================
    def build_table(self):
        table_frame = ttk.LabelFrame(self.root, text="Registered Donors", padding=10)
        table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # --- NEW: Simple Search Bar Layout ---
        search_frame = ttk.Frame(table_frame)
        search_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
        ttk.Label(search_frame, text="Search Name:").grid(row=0, column=0, padx=5)
        self.search_var = tk.StringVar()
        
        # When user types in search bar, call the filter_table function
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.grid(row=0, column=1, padx=5)
        
        # This triggers search dynamically as you type!
        self.search_var.trace_add("write", lambda *args: self.filter_table())

        # --- The Table View ---
        columns = ("name", "age", "blood_group", "contact")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)

        headings = {"name": "Name", "age": "Age", "blood_group": "Blood Group", "contact": "Contact"}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        
        # --- NEW: Delete Button ---
        ttk.Button(table_frame, text="Delete Selected", command=self.delete_donor).grid(row=2, column=0, sticky="e", pady=5)

    # ==========================================
    # 3) THE MATPLOTLIB CHART
    # ==========================================
    def build_chart(self):
        chart_frame = ttk.LabelFrame(self.root, text="Inventory Chart", padding=10)
        chart_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.figure = Figure(figsize=(8, 2.5), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ==========================================
    # APP ACTIONS LOGIC
    # ==========================================
    def add_donor(self):
        """Runs when you click Submit."""
        name = self.name_var.get().strip()
        age_text = self.age_var.get().strip()
        group = self.group_var.get()
        contact = self.contact_var.get().strip()

        # Basic validations
        if not name or not age_text or not group or not contact:
            messagebox.showwarning("Missing info", "Please fill in every box.")
            return
        if not age_text.isdigit():
            messagebox.showwarning("Invalid age", "Age must be a number.")
            return

        # Add dictionary data to our master list
        new_donor = {"name": name, "age": int(age_text), "blood_group": group, "contact": contact}
        self.donors.append(new_donor)

        # Refresh all views
        self.filter_table()
        self.refresh_chart()
        
        # Clear fields
        self.name_var.set("")
        self.age_var.set("")
        self.group_var.set("")
        self.contact_var.set("")

    def delete_donor(self):
        """Runs when you click Delete Selected."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Missing", "Click a row in the table first.")
            return
            
        # Get the row position index number
        selected_index = self.tree.index(selected_item)
        
        # Remove it from our simple python list using its position index
        self.donors.pop(selected_index)
        
        # Refresh the display views
        self.filter_table()
        self.refresh_chart()

    def filter_table(self):
        """Clears the table and re-displays donors matching search term."""
        # Step 1: Wipe the table clean
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        search_term = self.search_var.get().lower()

        # Step 2: Loop through list and insert only what matches search box
        for donor in self.donors:
            if search_term in donor["name"].lower():
                self.tree.insert("", tk.END, values=(donor["name"], donor["age"], donor["blood_group"], donor["contact"]))

    def refresh_chart(self):
        """Calculates totals and updates chart bar sizes."""
        # Simple loop counting logic
        counts = Counter(donor["blood_group"] for donor in self.donors)
        heights = [counts[group] for group in BLOOD_GROUPS]

        self.ax.clear()
        self.ax.bar(BLOOD_GROUPS, heights, color='#d9534f')
        self.ax.set_ylabel("Donors Count")
        
        self.canvas.draw()


# --- Start Window ---
if __name__ == "__main__":
    window = tk.Tk()
    app = BloodDonorApp(window)
    window.mainloop()
