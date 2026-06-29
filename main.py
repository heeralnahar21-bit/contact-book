import os
import json

class Contacts:
    def __init__(self,name,phone,email):
         
         self.name=name
         self.phone=phone
         self.email=email
    def to_dict(self):
         return{
         "name":self.name,
         "phone":self.phone,
         "email":self.email
              
         }

class Contactbook:
    def __init__(self):
        self.contacts=[]
    def add_contact(self,contact):
          self.contacts.append(contact)
    def viewcontacts(self):
         for contact in self.contacts:
              print(contact.name)
              print(contact.phone)
              print(contact.email)
    def search_contact(self,name):
        for contact in self.contacts:
            if contact.name.lower()==name.lower():
                print("contact found")
            else:
                 print("not found")
    def remove_contacts(self,name):
         for contact in self.contacts:
            if contact.name.lower()==name.lower():
                 self.contacts.remove(contact)
            else:
                 print("contact not found")
    def load_contacts(self):
        try:
            with open("contact.json","r") as file:
                  data=json.load(file)
            for contact in data["Contacts"]:
                 obj=Contacts(
                      contact["name"],
                      contact["phone number"],
                      contact["email"],
                 )
                 self.contacts.append(obj)
        except FileNotFoundError:
             self.contacts=[]
    def save_contacts(self):
        data=[]
        for contact in self.contacts:
            data.append(contact.to_dict())
            with open("contact.json","w") as file:
                json.dump(data,file,indent=4)
            print("contact saved succesfully")
if __name__ == "__main__":

    book=Contactbook()
    book.load_contacts()

    while True:
        print("\n----- Contact Book -----")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Remove Contact")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter Name: ")
            phone = input("Enter Phone: ")
            email = input("Enter Email: ")

            contact = Contacts(name, phone, email)
            book.add_contact(contact)
            book.save_contacts()

        elif choice == "2":
            book.viewcontacts()

        elif choice == "3":
            name = input("Enter Name to Search: ")
            book.search_contact(name)

        elif choice == "4":
            name = input("Enter Name to Remove: ")
            book.remove_contacts(name)
            book.save_contacts()

        elif choice == "5":
            print("Thank you!")
            break

        else:
            print("Invalid Choice")

              
             

             

              
         
            
              
              
    