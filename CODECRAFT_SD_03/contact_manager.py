import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import csv  # NEW: for CSV export

CONTACTS_FILE = 'contacts.json'

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)

def refresh_listbox():
    listbox.delete(0, tk.END)
    for contact in contacts:
        listbox.insert(tk.END, f"{contact['name']} | {contact['phone']} | {contact['email']}")

def add_contact():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    if name and phone and email:
        contacts.append({'name': name, 'phone': phone, 'email': email})
        save_contacts(contacts)
        refresh_listbox()
        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        messagebox.showinfo("Success", "Contact added!")
    else:
        messagebox.showwarning("Input Error", "All fields are required!")

def edit_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a contact to edit.")
        return

    index = selected[0]
    contact = contacts[index]

    name = simpledialog.askstring("Edit Name", "Enter new name:", initialvalue=contact['name'])
    phone = simpledialog.askstring("Edit Phone", "Enter new phone:", initialvalue=contact['phone'])
    email = simpledialog.askstring("Edit Email", "Enter new email:", initialvalue=contact['email'])

    if name and phone and email:
        contacts[index] = {'name': name, 'phone': phone, 'email': email}
        save_contacts(contacts)
        refresh_listbox()
        messagebox.showinfo("Success", "Contact updated!")
    else:
        messagebox.showwarning("Input Error", "All fields must be filled.")

def delete_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a contact to delete.")
        return

    index = selected[0]
    confirm = messagebox.askyesno("Confirm Delete", f"Delete contact: {contacts[index]['name']}?")
    if confirm:
        contacts.pop(index)
        save_contacts(contacts)
        refresh_listbox()
        messagebox.showinfo("Deleted", "Contact deleted.")

# ✅ NEW: Export contacts to CSV file
def export_to_csv():
    if not contacts:
        messagebox.showwarning("No Contacts", "No contacts available to export.")
        return
    try:
        with open("contacts.csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["name", "phone", "email"])
            writer.writeheader()
            for contact in contacts:
                writer.writerow(contact)
        messagebox.showinfo("Exported", "Contacts exported to 'contacts.csv' successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export contacts.\n{e}")

# Load contacts initially
contacts = load_contacts()

# Setup GUI
root = tk.Tk()
root.title("Contact Management System")

# Input fields
tk.Label(root, text="Name").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Phone").grid(row=1, column=0, padx=5, pady=5)
entry_phone = tk.Entry(root)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Email").grid(row=2, column=0, padx=5, pady=5)
entry_email = tk.Entry(root)
entry_email.grid(row=2, column=1, padx=5, pady=5)

tk.Button(root, text="Add Contact", command=add_contact).grid(row=3, column=0, columnspan=2, pady=10)

# Contact list
listbox = tk.Listbox(root, width=50)
listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Buttons for edit/delete
tk.Button(root, text="Edit Contact", command=edit_contact).grid(row=5, column=0, pady=5)
tk.Button(root, text="Delete Contact", command=delete_contact).grid(row=5, column=1, pady=5)

# ✅ NEW: Export to CSV button
tk.Button(root, text="Export to CSV", command=export_to_csv).grid(row=6, column=0, columnspan=2, pady=10)

# Initial list population
refresh_listbox()

# Run the app
root.mainloop()
