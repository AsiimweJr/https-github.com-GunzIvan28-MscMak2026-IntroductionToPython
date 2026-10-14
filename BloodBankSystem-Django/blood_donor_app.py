"""
Graphical blood donor registry with search and a blood-group count chart.

The app lets users add donors, filter and delete records, and view donor counts
by blood group. Records are kept in memory and are cleared when the app closes.

Run from the ``blood_bank`` directory with ``python -m scripts.blood_donor_app``
or ``python scripts/blood_donor_app.py``. Install Matplotlib with
``python -m pip install matplotlib``.
"""
# Author: AsiimweJr

import tkinter as tk
from tkinter import messagebox, ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# try:
#     if __package__:
#         from .shared_constants import BLOOD_GROUPS
#     else:
#         from shared_constants import BLOOD_GROUPS
# except ImportError:
BLOOD_GROUPS = ("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-")


class DonorRegistry:
    """In-memory donor store and blood-group inventory used by the GUI."""

    def __init__(self):
        self.donor_list = []
        self.blood_inventory = {group: 0 for group in BLOOD_GROUPS}

    def add_donor(self, name, age, blood_group, contact):
        donor = {
            "name": name,
            "age": age,
            "blood": blood_group,
            "contact": contact,
        }
        self.donor_list.append(donor)
        self.blood_inventory[blood_group] += 1
        return donor

    def delete_donor(self, index):
        donor = self.donor_list.pop(index)
        self.blood_inventory[donor["blood"]] -= 1
        return donor


class BloodDonorApp:
    """
    This class holds everything for our Blood Donor Registry app.
    When we create an object of this class, the whole window is built.
    """

    def __init__(self, root):
        """
        This special method runs automatically when we create the app.
        'root' is the main window that tkinter gives us.
        """
        self.root = root
        self.root.title("Blood Donor Registry")   # Title that appears at the top of the window
        self.root.geometry("1000x650")             # Width x Height of the window

        self.registry = DonorRegistry()

        # Build the three main parts of the screen
        self.build_form()    # Left side: form to add a new donor
        self.build_table()   # Right side: table + search bar
        self.build_chart()   # Bottom: bar chart of blood groups
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Draw the (empty) chart when the app first starts
        self.refresh_chart()


    
    # 4. BUILD THE "ADD NEW DONOR" FORM (left side)
    
    def build_form(self):
        """Creates the form where the user types new donor information."""

        # A labelled box that groups all the form widgets together
        form = ttk.LabelFrame(self.root, text="Add New Donor", padding=10)
        form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # These variables are connected to the entry boxes.
        # When the user types, these variables automatically update.
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.group_var = tk.StringVar()
        self.contact_var = tk.StringVar()

        # ---- Name ----
        ttk.Label(form, text="Donor Name:").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.name_var, width=25).grid(row=0, column=1, pady=4)

        # ---- Age ----
        ttk.Label(form, text="Age:").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.age_var, width=25).grid(row=1, column=1, pady=4)

        # ---- Blood Group (dropdown menu) ----
        ttk.Label(form, text="Blood Group:").grid(row=2, column=0, sticky="w", pady=4)
        blood_combo = ttk.Combobox(
            form,
            textvariable=self.group_var,
            values=BLOOD_GROUPS,      # the list we defined at the top
            state="readonly",         # user can only choose, not type freely
            width=22
        )
        blood_combo.grid(row=2, column=1, pady=4)

        # ---- Contact Info ----
        ttk.Label(form, text="Contact Info:").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.contact_var, width=25).grid(row=3, column=1, pady=4)

        # ---- Submit Button ----
        # When clicked, it calls the method self.add_donor
        ttk.Button(form, text="Submit Donor", command=self.add_donor).grid(
            row=4, column=0, columnspan=2, pady=12
        )


    
    # 5. BUILD THE TABLE + SEARCH BAR (right side)
    
    def build_table(self):
        """Creates the table that shows all registered donors and the search bar."""

        table_frame = ttk.LabelFrame(self.root, text="Registered Donors", padding=10)
        table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # ---------- Search bar ----------
        search_frame = ttk.Frame(table_frame)
        search_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

        ttk.Label(search_frame, text="Search Name:").grid(row=0, column=0, padx=5)

        self.search_var = tk.StringVar()

        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.grid(row=0, column=1, padx=5)

        # This line makes the table update automatically
        # every time the user types a letter in the search box.
        # "write" means "when the text changes".
        self.search_var.trace_add("write", self.filter_table)

        # ---------- The table itself ----------
        # columns = the internal names of each column
        columns = ("name", "age", "blood_group", "contact")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",   # hide the first empty column
            height=8           # show 8 rows at a time
        )

        # Friendly names that the user sees at the top of each column
        headings = {
            "name": "Name",
            "age": "Age",
            "blood_group": "Blood Group",
            "contact": "Contact"
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=100, anchor="center")

        # Vertical scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        # ---------- Delete button ----------
        ttk.Button(
            table_frame,
            text="Delete Selected",
            command=self.delete_donor
        ).grid(row=2, column=0, sticky="e", pady=5)


    # 6. BUILD THE CHART 
    def build_chart(self):
        """Creates an empty matplotlib chart that we will later fill with data."""

        chart_frame = ttk.LabelFrame(self.root, text="Inventory Chart", padding=10)
        chart_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Create a matplotlib Figure (the canvas we draw on)
        self.figure = Figure(figsize=(8, 2.5), dpi=100)

        # Add one set of axes to the figure
        self.ax = self.figure.add_subplot(111)

        # Put the matplotlib figure inside the tkinter window
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)


    # 7. APP ACTIONS (the real logic)
    

    def add_donor(self):
        """
        This runs when the user clicks the "Submit Donor" button.
        It checks the data, saves the new donor, and refreshes the screen.
        """
        # Get the text the user typed and remove extra spaces
        name = self.name_var.get().strip()
        age_text = self.age_var.get().strip()
        group = self.group_var.get()
        contact = self.contact_var.get().strip()

        # ----- Validation -----
        # Check that nothing is empty
        if not name or not age_text or not group or not contact:
            messagebox.showwarning("Missing info", "Please fill in every box.")
            return   # stop the function early

        # Check that age is a whole number
        if not age_text.isdigit():
            messagebox.showwarning("Invalid age", "Age must be a number.")
            return

        if group not in BLOOD_GROUPS:
            messagebox.showwarning("Invalid blood group", "Choose a valid blood group.")
            return

        age = int(age_text)
        if age <= 0:
            messagebox.showwarning("Invalid age", "Age must be a positive number.")
            return

        self.registry.add_donor(name, age, group, contact)

        # Update the table and the chart so the user sees the change
        self.filter_table()
        self.refresh_chart()

        # Clear all the entry boxes so they are ready for the next donor
        self.name_var.set("")
        self.age_var.set("")
        self.group_var.set("")
        self.contact_var.set("")


    def delete_donor(self):
        """
        This runs when the user clicks "Delete Selected".
        It removes the highlighted row from both the table and the list.
        """
        selection = self.tree.selection()

        if not selection:
            messagebox.showwarning("Selection Missing", "Click a row in the table first.")
            return

        selected_item = selection[0]

        try:
            selected_index = int(selected_item)
        except (TypeError, ValueError):
            selected_index = self.tree.index(selected_item)

        self.registry.delete_donor(selected_index)
        self.filter_table()
        self.refresh_chart()


    def filter_table(self, *_):
        """
        Clears the table and then re-fills it with only the donors
        whose name contains the search text.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_term = self.search_var.get().lower()

        for index, donor in enumerate(self.registry.donor_list):
            if search_term in donor["name"].lower():
                self.tree.insert(
                    "",
                    tk.END,
                    iid=str(index),
                    values=(
                        donor["name"],
                        donor["age"],
                        donor["blood"],
                        donor["contact"]
                    )
                )


    def refresh_chart(self):
        """
        Counts how many donors have each blood group
        and redraws the bar chart.
        """
        heights = [self.registry.blood_inventory[group] for group in BLOOD_GROUPS]

        # Clear the old bars
        self.ax.clear()

        # Draw new bars (red colour)
        self.ax.bar(BLOOD_GROUPS, heights, color="#d9534f")

        # Label for the vertical axis
        self.ax.set_ylabel("Donors Count")
        self.ax.set_title("Registered donors by blood group")
        self.ax.set_ylim(bottom=0)

        # Tell the canvas to show the updated chart
        self.canvas.draw()



def main() -> None:
    """Create and run the application window."""
    window = tk.Tk()
    BloodDonorApp(window)
    window.mainloop()


if __name__ == "__main__":
    main()
