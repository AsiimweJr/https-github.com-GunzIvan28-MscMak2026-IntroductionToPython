"""Blood Donor Registry and Inventory Visualizer desktop app.

This is a beginner-friendly desktop app made with tkinter and matplotlib.
It has:
- an input form for donor details
- a table to display donor records
- a bar chart showing donor counts by blood group

The code is written in a simple, step-by-step way so a beginner can follow it.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib

# Make Matplotlib use the Tkinter backend so it can draw inside the window.
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# This list is used for all blood group choices.
BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


class DonorRegistry:
    """Stores donor data in a simple list."""

    def __init__(self):
        # Each donor is stored as a dictionary.
        # Example:
        # {"name": "Alice", "age": 26, "blood_group": "O+", "contact": "0756782345"}
        self.donors = []

    def add_donor(self, name, age, blood_group, contact):
        """Add one donor to the list."""
        donor = {
            "name": name,
            "age": age,
            "blood_group": blood_group,
            "contact": contact,
        }
        self.donors.append(donor)

    def count_by_blood_group(self):
        """Return a dictionary with the number of donors in each blood group."""
        counts = {group: 0 for group in BLOOD_GROUPS}

        for donor in self.donors:
            group = donor["blood_group"]
            counts[group] = counts.get(group, 0) + 1

        return counts


class DonorApp(tk.Tk):
    """This class builds the main window and connects the widgets to the logic."""

    def __init__(self):
        super().__init__()

        self.title("Blood Donor Registry")
        self.geometry("1150x700")

        # Create the data store for this app.
        self.registry = DonorRegistry()

        # StringVar objects hold the text typed into the form.
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.blood_group_var = tk.StringVar(value="A+")
        self.contact_var = tk.StringVar()

        # Build the user interface.
        self.build_gui()

        # Show the current table and chart immediately.
        self.refresh_table()
        self.refresh_chart()

    def build_gui(self):
        """Create the form, table, and chart widgets."""
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --------------------------------------------------
        # Left side: donor form
        # --------------------------------------------------
        form_frame = ttk.LabelFrame(main_frame, text="Add Donor", padding=12)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Entry(form_frame, textvariable=self.name_var, width=30).grid(
            row=0, column=1, sticky="ew", pady=6
        )

        ttk.Label(form_frame, text="Age:").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(form_frame, textvariable=self.age_var, width=30).grid(
            row=1, column=1, sticky="ew", pady=6
        )

        ttk.Label(form_frame, text="Blood Group:").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Combobox(
            form_frame,
            textvariable=self.blood_group_var,
            values=BLOOD_GROUPS,
            state="readonly",
            width=27,
        ).grid(row=2, column=1, sticky="ew", pady=6)

        ttk.Label(form_frame, text="Contact Info:").grid(row=3, column=0, sticky="w", pady=6)
        ttk.Entry(form_frame, textvariable=self.contact_var, width=30).grid(
            row=3, column=1, sticky="ew", pady=6
        )

        ttk.Button(form_frame, text="Submit Donor", command=self.submit_donor).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=(18, 0)
        )

        form_frame.columnconfigure(1, weight=1)

        # --------------------------------------------------
        # Right side: donor table and chart
        # --------------------------------------------------
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew")

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3)
        main_frame.rowconfigure(0, weight=1)

        # Treeview table for donor records.
        table_frame = ttk.LabelFrame(right_frame, text="Donor Records", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("name", "age", "blood_group", "contact"),
            show="headings",
        )

        self.tree.heading("name", text="Name")
        self.tree.heading("age", text="Age")
        self.tree.heading("blood_group", text="Blood Group")
        self.tree.heading("contact", text="Contact Info")

        self.tree.column("name", width=180, anchor="center")
        self.tree.column("age", width=80, anchor="center")
        self.tree.column("blood_group", width=120, anchor="center")
        self.tree.column("contact", width=220, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Matplotlib chart for inventory counts.
        chart_frame = ttk.LabelFrame(right_frame, text="Inventory Visualizer", padding=10)
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.figure = Figure(figsize=(5.5, 3.5), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def submit_donor(self):
        """Read the form, validate it, and save the donor."""
        name = self.name_var.get().strip()
        age_text = self.age_var.get().strip()
        blood_group = self.blood_group_var.get()
        contact = self.contact_var.get().strip()

        # Check if the name is empty.
        if not name:
            messagebox.showerror("Missing name", "Please type the donor's name.")
            return

        # Check if the contact info is empty.
        if not contact:
            messagebox.showerror("Missing contact", "Please type the donor's contact information.")
            return

        # Try to convert the age to an integer.
        try:
            age = int(age_text)
        except ValueError:
            messagebox.showerror("Invalid age", "Age must be a whole number.")
            return

        # Age must be positive.
        if age <= 0:
            messagebox.showerror("Invalid age", "Age must be greater than zero.")
            return

        # Save donor in the registry.
        self.registry.add_donor(name, age, blood_group, contact)

        # Clear the form after a successful save.
        self.name_var.set("")
        self.age_var.set("")
        self.contact_var.set("")
        self.blood_group_var.set("A+")

        # Refresh the displayed table and chart.
        self.refresh_table()
        self.refresh_chart()

        messagebox.showinfo("Success", f"{name} was added to the donor registry.")

    def refresh_table(self):
        """Show all donor records in the Treeview table."""
        # Remove the old rows before drawing the new list.
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert each donor from the registry into the table.
        for donor in self.registry.donors:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    donor["name"],
                    donor["age"],
                    donor["blood_group"],
                    donor["contact"],
                ),
            )

    def refresh_chart(self):
        """Rebuild the bar chart from the current donor data."""
        counts = self.registry.count_by_blood_group()
        groups = list(counts.keys())
        values = list(counts.values())

        # Clear the old chart so it can be redrawn.
        self.ax.clear()

        # Use green bars for blood groups with donors, grey for empty ones.
        colors = ["#2E8B57" if value > 0 else "#D9D9D9" for value in values]
        self.ax.bar(groups, values, color=colors)

        self.ax.set_title("Donor Counts by Blood Group")
        self.ax.set_xlabel("Blood Group")
        self.ax.set_ylabel("Number of Donors")
        self.ax.set_ylim(0, max(5, max(values) + 1))
        self.ax.grid(axis="y", linestyle="--", alpha=0.5)
        self.ax.tick_params(axis="x", rotation=45)

        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = DonorApp()
    app.mainloop()
