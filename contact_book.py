# contact_book.py - Complete Contact Book Application
# CODSOFT Python Programming Internship - Task 5

import json
import os
import re

# File to store contacts
CONTACTS_FILE = "contacts.json"
contacts = []

# ========== FILE HANDLING ==========

def load_contacts():
    """Load contacts from file"""
    global contacts
    
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, 'r') as file:
                contacts = json.load(file)
                print("Loaded " + str(len(contacts)) + " contacts")
        except:
            print("Error loading contacts. Starting fresh.")
            contacts = []
    else:
        print("No saved contacts found. Starting fresh.")
        contacts = []

def save_contacts():
    """Save contacts to file"""
    try:
        with open(CONTACTS_FILE, 'w') as file:
            json.dump(contacts, file, indent=4)
        print("Contacts saved successfully!")
    except:
        print("Error saving contacts!")

# ========== VALIDATION FUNCTIONS ==========

def validate_phone(phone):
    """Validate phone number (10 digits)"""
    return re.match(r'^[0-9]{10}$', phone) is not None

def validate_email(email):
    """Validate email format"""
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

def get_next_id():
    """Get next available ID"""
    if not contacts:
        return 1
    else:
        max_id = max(contact["id"] for contact in contacts)
        return max_id + 1

# ========== CONTACT OPERATIONS ==========

def add_contact():
    """Add a new contact"""
    print("\n" + "="*40)
    print("ADD NEW CONTACT")
    print("="*40)
    
    name = input("Enter name: ").strip()
    if not name:
        print("Name cannot be empty!")
        return
    
    while True:
        phone = input("Enter phone number (10 digits): ").strip()
        if validate_phone(phone):
            for contact in contacts:
                if contact["phone"] == phone:
                    print("This phone number already exists!")
                    return
            break
        else:
            print("Invalid phone number! Please enter 10 digits only.")
    
    while True:
        email = input("Enter email: ").strip()
        if not email:
            print("Email cannot be empty!")
            continue
        if validate_email(email):
            break
        else:
            print("Invalid email format! (e.g., name@example.com)")
    
    address = input("Enter address: ").strip()
    if not address:
        print("Address cannot be empty!")
        return
    
    contact = {
        "id": get_next_id(),
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    }
    
    contacts.append(contact)
    save_contacts()
    print("\nContact added successfully!")
    print("ID: " + str(contact["id"]))

def view_all_contacts():
    """View all contacts"""
    if not contacts:
        print("\nNo contacts found!")
        return
    
    print("\n" + "="*70)
    print("ALL CONTACTS")
    print("="*70)
    print("ID  | NAME                | PHONE      | EMAIL")
    print("-"*70)
    
    for contact in contacts:
        name = contact["name"][:18].ljust(18)
        print(str(contact["id"]).ljust(3) + " | " + name + " | " + contact["phone"] + " | " + contact["email"])
    
    print("="*70)
    print("Total contacts: " + str(len(contacts)))

def search_contact():
    """Search for a contact by name or phone"""
    if not contacts:
        print("\nNo contacts found!")
        return
    
    print("\n" + "="*40)
    print("SEARCH CONTACT")
    print("="*40)
    
    search_term = input("Enter name or phone to search: ").strip().lower()
    
    if not search_term:
        print("Search term cannot be empty!")
        return
    
    results = []
    for contact in contacts:
        if search_term in contact["name"].lower() or search_term in contact["phone"]:
            results.append(contact)
    
    if not results:
        print("No contacts found matching '" + search_term + "'")
        return
    
    print("\n" + "="*70)
    print("SEARCH RESULTS")
    print("="*70)
    print("ID  | NAME                | PHONE      | EMAIL")
    print("-"*70)
    
    for contact in results:
        name = contact["name"][:18].ljust(18)
        print(str(contact["id"]).ljust(3) + " | " + name + " | " + contact["phone"] + " | " + contact["email"])
    
    print("="*70)
    print("Found " + str(len(results)) + " contact(s)")

def view_contact_details():
    """View full details of a specific contact"""
    if not contacts:
        print("\nNo contacts found!")
        return
    
    view_all_contacts()
    
    try:
        contact_id = int(input("\nEnter contact ID to view details: "))
        
        for contact in contacts:
            if contact["id"] == contact_id:
                print("\n" + "="*50)
                print("CONTACT DETAILS")
                print("="*50)
                print("ID:      " + str(contact["id"]))
                print("Name:    " + contact["name"])
                print("Phone:   " + contact["phone"])
                print("Email:   " + contact["email"])
                print("Address: " + contact["address"])
                print("="*50)
                return
        
        print("Contact with ID " + str(contact_id) + " not found!")
    except ValueError:
        print("Invalid input! Please enter a number.")

def update_contact():
    """Update an existing contact"""
    if not contacts:
        print("\nNo contacts found!")
        return
    
    view_all_contacts()
    
    try:
        contact_id = int(input("\nEnter contact ID to update: "))
        
        for contact in contacts:
            if contact["id"] == contact_id:
                print("\nLeave blank to keep current value")
                print("Current name: " + contact["name"])
                name = input("New name: ").strip()
                if name:
                    contact["name"] = name
                
                print("Current phone: " + contact["phone"])
                while True:
                    phone = input("New phone (10 digits): ").strip()
                    if not phone:
                        break
                    if validate_phone(phone):
                        for c in contacts:
                            if c["phone"] == phone and c["id"] != contact_id:
                                print("This phone number already exists for another contact!")
                                return
                        contact["phone"] = phone
                        break
                    else:
                        print("Invalid phone number! Please enter 10 digits only.")
                
                print("Current email: " + contact["email"])
                while True:
                    email = input("New email: ").strip()
                    if not email:
                        break
                    if validate_email(email):
                        contact["email"] = email
                        break
                    else:
                        print("Invalid email format!")
                
                print("Current address: " + contact["address"])
                address = input("New address: ").strip()
                if address:
                    contact["address"] = address
                
                save_contacts()
                print("\nContact updated successfully!")
                return
        
        print("Contact with ID " + str(contact_id) + " not found!")
    except ValueError:
        print("Invalid input! Please enter a number.")

def delete_contact():
    """Delete a contact"""
    if not contacts:
        print("\nNo contacts found!")
        return
    
    view_all_contacts()
    
    try:
        contact_id = int(input("\nEnter contact ID to delete: "))
        
        for i, contact in enumerate(contacts):
            if contact["id"] == contact_id:
                confirm = input("Are you sure you want to delete '" + contact["name"] + "'? (y/n): ")
                if confirm.lower() == 'y':
                    deleted_contact = contacts.pop(i)
                    save_contacts()
                    print("Contact '" + deleted_contact["name"] + "' deleted successfully!")
                else:
                    print("Deletion cancelled.")
                return
        
        print("Contact with ID " + str(contact_id) + " not found!")
    except ValueError:
        print("Invalid input! Please enter a number.")

def delete_all_contacts():
    """Delete all contacts"""
    global contacts  # <-- THIS MUST BE THE FIRST LINE AFTER DOCSTRING
    
    if not contacts:
        print("\nNo contacts to delete!")
        return
    
    confirm = input("Are you sure you want to delete ALL contacts? This cannot be undone! (y/n): ")
    if confirm.lower() == 'y':
        contacts = []
        save_contacts()
        print("All contacts deleted successfully!")
    else:
        print("Operation cancelled.")

# ========== STATISTICS ==========

def show_statistics():
    """Show contact statistics"""
    if not contacts:
        print("\nNo contacts to analyze!")
        return
    
    print("\n" + "="*40)
    print("CONTACT STATISTICS")
    print("="*40)
    print("Total contacts: " + str(len(contacts)))
    
    # Most common name prefix
    names = []
    for contact in contacts:
        if contact["name"] and " " in contact["name"]:
            names.append(contact["name"].split()[0])
    
    if names:
        most_common = max(set(names), key=names.count)
        print("Most common first name: " + most_common)
    
    # Domain count
    domains = {}
    for contact in contacts:
        if "@" in contact["email"]:
            domain = contact["email"].split("@")[1]
            domains[domain] = domains.get(domain, 0) + 1
    
    if domains:
        print("\nEmail domains:")
        for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
            print("  " + domain + ": " + str(count) + " contact(s)")
    
    print("="*40)

# ========== MAIN MENU ==========

def main():
    """Main program loop"""
    load_contacts()
    
    while True:
        print("\n" + "="*50)
        print("CONTACT BOOK APPLICATION")
        print("="*50)
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contact")
        print("4. View Contact Details")
        print("5. Update Contact")
        print("6. Delete Contact")
        print("7. Delete All Contacts")
        print("8. View Statistics")
        print("9. Exit")
        print("="*50)
        
        choice = input("Choose option (1-9): ")
        
        if choice == '1':
            add_contact()
        elif choice == '2':
            view_all_contacts()
        elif choice == '3':
            search_contact()
        elif choice == '4':
            view_contact_details()
        elif choice == '5':
            update_contact()
        elif choice == '6':
            delete_contact()
        elif choice == '7':
            delete_all_contacts()
        elif choice == '8':
            show_statistics()
        elif choice == '9':
            save_contacts()
            print("\nGoodbye! Thanks for using Contact Book!")
            break
        else:
            print("Invalid option! Please choose 1-9.")

if __name__ == "__main__":
    main()