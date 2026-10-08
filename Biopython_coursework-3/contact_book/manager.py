"""Functions for using the contact book."""

from .storage import load_contacts, save_contacts


contacts = load_contacts()


def is_valid_phone_number(phone_number):
    """Check that the phone number has at least seven digits."""
    digit_count = 0

    for character in phone_number:
        if character.isdigit():
            digit_count += 1
        elif character not in "+()- ":
            return False

    return digit_count >= 7


def add_contact():
    """Ask for a name and phone number, then save the contact."""
    name = input("Enter contact name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    for saved_name in contacts:
        if saved_name.lower() == name.lower():
            print("That name is already in the contact book.")
            return

    phone = input("Enter phone number: ").strip()
    if not phone:
        print("Phone number cannot be empty.")
        return

    if not is_valid_phone_number(phone):
        print("Enter a valid phone number with at least seven digits.")
        return

    contacts[name] = phone
    save_contacts(contacts)
    print("Contact added.")


def view_contacts():
    """Print all saved contacts."""
    if not contacts:
        print("The contact book is empty.")
        return

    print("Name                 | Phone Number")
    print("---------------------|-------------")

    for name in sorted(contacts):
        print(name, "|", contacts[name])


def search_contact():
    """Find and print one contact by name."""
    name = input("Enter the name to search for: ").strip()

    if name in contacts:
        print(name, ":", contacts[name])
    else:
        print("Contact not found.")


def delete_contact():
    """Ask before removing a contact."""
    name = input("Enter the name to delete: ").strip()

    if name not in contacts:
        print("Contact not found.")
        return

    answer = input("Delete " + name + "? (y/n): ").strip().lower()
    if answer == "y":
        del contacts[name]
        save_contacts(contacts)
        print("Contact deleted.")
    else:
        print("Deletion cancelled.")


def main_menu():
    """Show the menu and run the selected action."""
    while True:
        print("\nCONTACT BOOK")
        print("1. Add a contact")
        print("2. View contacts")
        print("3. Search for a contact")
        print("4. Delete a contact")
        print("5. Exit")

        choice = input("Choose 1 to 5: ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Please choose a number from 1 to 5.")
