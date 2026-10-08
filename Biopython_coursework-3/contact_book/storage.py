"""Save and load contacts from a JSON file."""

import json
import os


DATA_FILE = "results/contacts_data.json"


def load_contacts():
    """Read saved contacts. Return an empty dictionary if there is no file."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_contacts(contacts):
    """Write contacts to the JSON file."""
    os.makedirs("results", exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)
