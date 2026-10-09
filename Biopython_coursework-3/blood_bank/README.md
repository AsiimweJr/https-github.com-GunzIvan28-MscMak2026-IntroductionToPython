# Blood Donor Registry and Inventory Visualizer

A beginner-friendly desktop application for registering blood donors. It
displays donor records in a table and shows how many registered donors belong
to each blood group in a bar chart.

## What the app does

- Collects a donor's name, age, blood group, and contact information.
- Lets the user select from A+, A-, B+, B-, AB+, AB-, O+, and O-.
- Checks that name and contact information are entered and that age is a
  positive whole number.
- Displays saved records in a table.
- Refreshes the chart after each donor is added.

The chart counts **donors** by blood group. It does not track units of donated
blood or medical inventory.

## Files in this folder

- `blood_donor_registry_app.py` - the application code.
- `requirements.txt` - the Matplotlib package required for the chart.

## Requirements

- Python 3
- Tkinter, which is included with many Python installations
- Matplotlib

On some Linux systems, Tkinter must be installed separately. For Debian or
Ubuntu, install it with:

```bash
sudo apt install python3-tk
```

## Set up and run on Linux or macOS

Open a terminal in the project folder, then enter the app folder:

```bash
cd blood_bank
```

Create a virtual environment. This keeps the app's installed packages separate
from other Python projects:

```bash
python3 -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

Install Matplotlib and run the program:

```bash
python -m pip install -r requirements.txt
python blood_donor_registry_app.py
```

When you are finished, you can leave the virtual environment by entering:

```bash
deactivate
```

## How the code works

1. `DonorRegistry` keeps donor records in a Python list while the app is open.
2. `DonorApp` builds the form, table, and chart window.
3. Clicking **Submit Donor** checks the form and adds a valid donor to the list.
4. The app refreshes the table and recounts donors for the chart.

The records are only kept in memory. Closing the app removes them; this simple
version does not save records to a file or database.
