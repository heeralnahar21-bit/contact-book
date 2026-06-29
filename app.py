import os
import json
import streamlit as st

# ── Original classes (unchanged logic, bugs fixed) ─────────────────────────────

class Contacts:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }


class Contactbook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def viewcontacts(self):
        return self.contacts  # return list instead of print

    def search_contact(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                return contact          # return found contact
        return None                     # return None if not found

    def remove_contacts(self, name):
        # fixed: don't mutate list while iterating
        original_len = len(self.contacts)
        self.contacts = [c for c in self.contacts if c.name.lower() != name.lower()]
        return len(self.contacts) < original_len  # True if something was removed

    def load_contacts(self):
        try:
            with open("contact.json", "r") as file:
                data = json.load(file)
            for contact in data["Contacts"]:
                obj = Contacts(
                    contact["name"],
                    contact["phone"],
                    contact["email"],
                )
                self.contacts.append(obj)
        except FileNotFoundError:
            self.contacts = []

    def save_contacts(self):
        data = []
        for contact in self.contacts:
            data.append(contact.to_dict())
        # fixed: json.dump was inside the loop before
        with open("contacts.json", "w") as file:
            json.dump(data, file, indent=4)


# ── Streamlit UI ───────────────────────────────────────────────────────────────

st.set_page_config(page_title="Contact Book", page_icon="📒", layout="wide")

# Load once into session state
if "book" not in st.session_state:
    book = Contactbook()
    book.load_contacts()
    st.session_state.book = book

book: Contactbook = st.session_state.book

st.title("📒 Contact Book")
st.divider()

menu = st.sidebar.radio(
    "Menu",
    ["View Contacts", "Add Contact", "Search Contact", "Remove Contact"]
)

# ── 1. View Contacts ───────────────────────────────────────────────────────────
if menu == "View Contacts":
    st.subheader("All Contacts")
    contacts = book.viewcontacts()

    if not contacts:
        st.info("No contacts yet. Add one from the menu!")
    else:
        for contact in contacts:
            with st.container(border=True):
                col1, col2 = st.columns(2)
                col1.markdown(f"**👤 Name**\n\n{contact.name}")
                col2.markdown(f"**📞 Phone**\n\n{contact.phone}")
                st.markdown(f"**✉️ Email:** {contact.email}")

# ── 2. Add Contact ─────────────────────────────────────────────────────────────
elif menu == "Add Contact":
    st.subheader("Add Contact")

    name  = st.text_input("Name")
    phone = st.text_input("Phone")
    email = st.text_input("Email")

    if st.button("Add", type="primary"):
        if not name.strip():
            st.error("Name is required.")
        elif not phone.strip():
            st.error("Phone is required.")
        else:
            contact = Contacts(name.strip(), phone.strip(), email.strip())
            book.add_contact(contact)
            book.save_contacts()
            st.success(f"Contact **{name}** added successfully!")

# ── 3. Search Contact ──────────────────────────────────────────────────────────
elif menu == "Search Contact":
    st.subheader("Search Contact")

    name = st.text_input("Enter name to search")

    if st.button("Search"):
        result = book.search_contact(name.strip())
        if result:
            st.success("Contact found!")
            with st.container(border=True):
                st.markdown(f"**👤 Name:** {result.name}")
                st.markdown(f"**📞 Phone:** {result.phone}")
                st.markdown(f"**✉️ Email:** {result.email}")
        else:
            st.error("Contact not found.")

# ── 4. Remove Contact ──────────────────────────────────────────────────────────
elif menu == "Remove Contact":
    st.subheader("Remove Contact")

    name = st.text_input("Enter name to remove")

    if st.button("Remove", type="primary"):
        removed = book.remove_contacts(name.strip())
        if removed:
            book.save_contacts()
            st.success(f"Contact **{name}** removed successfully!")
        else:
            st.error("Contact not found.")