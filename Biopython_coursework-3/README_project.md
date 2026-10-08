# Contact Book Project

This project is a simple console-based contact book application written in Python.

## Purpose

The program allows users to:
- add a new contact
- view all saved contacts
- search by name
- delete a contact
- exit the application

## Project structure

- `cli.py` – command-line entry point
- `contact_book/manager.py` – asks what you want to do and handles the menu
- `contact_book/storage.py` – saves and reads the contact list
- `results/contacts_data.json` – saved contacts

## Run the program

Open a terminal in the project directory and run this Python command:

```text
python cli.py
```

## Notes

- The program uses Python files (`.py`) and Python's built-in tools.
- Contacts are kept in a JSON file so they are still there next time you run the program.
