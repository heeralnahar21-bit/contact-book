import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;

import java.io.*;
import java.lang.reflect.Type;
import java.util.*;

class Contact {
    String name;
    String phone;
    String email;

    Contact(String name, String phone, String email) {
        this.name = name;
        this.phone = phone;
        this.email = email;
    }
}

public class ContactBook {

    private static final String FILE = "contact.json";

    private static final Gson gson =
            new GsonBuilder().setPrettyPrinting().create();

    private static final Type CONTACT_LIST_TYPE =
            new TypeToken<ArrayList<Contact>>() {}.getType();

    private static ArrayList<Contact> contacts = new ArrayList<>();
    private static final Scanner sc = new Scanner(System.in);

    static void loadContacts() {
        File file = new File(FILE);

        if (!file.exists()) {
            return;
        }

        try (Reader reader = new FileReader(file)) {
            ArrayList<Contact> loaded =
                    gson.fromJson(reader, CONTACT_LIST_TYPE);

            if (loaded != null) {
                contacts = loaded;
            }

        } catch (IOException e) {
            System.out.println("Error loading contacts: " + e.getMessage());
        }
    }

    static void saveContacts() {
        try (Writer writer = new FileWriter(FILE)) {
            gson.toJson(contacts, CONTACT_LIST_TYPE, writer);

        } catch (IOException e) {
            System.out.println("Error saving contacts: " + e.getMessage());
        }
    }

    static void addContact() {
        System.out.print("Enter Name: ");
        String name = sc.nextLine();

        System.out.print("Enter Phone: ");
        String phone = sc.nextLine();

        System.out.print("Enter Email: ");
        String email = sc.nextLine();

        contacts.add(new Contact(name, phone, email));
        saveContacts();

        System.out.println("Contact added successfully!");
    }

    static void viewContacts() {
        if (contacts.isEmpty()) {
            System.out.println("No contacts found.");
            return;
        }

        for (Contact c : contacts) {
            System.out.println("Name: " + c.name);
            System.out.println("Phone: " + c.phone);
            System.out.println("Email: " + c.email);
            System.out.println("----------------------");
        }
    }

    static void searchContact() {
        System.out.print("Enter name to search: ");
        String name = sc.nextLine();

        boolean found = false;

        for (Contact c : contacts) {
            if (c.name.equalsIgnoreCase(name)) {
                System.out.println("Name: " + c.name);
                System.out.println("Phone: " + c.phone);
                System.out.println("Email: " + c.email);
                found = true;
            }
        }

        if (!found) {
            System.out.println("Contact not found.");
        }
    }

    static void removeContact() {
        System.out.print("Enter name to remove: ");
        String name = sc.nextLine();

        boolean removed = contacts.removeIf(
                c -> c.name.equalsIgnoreCase(name)
        );

        if (removed) {
            saveContacts();
            System.out.println("Contact removed successfully!");
        } else {
            System.out.println("Contact not found.");
        }
    }

    public static void main(String[] args) {
        loadContacts();

        while (true) {
            System.out.println("\n===== CONTACT BOOK =====");
            System.out.println("1. Add Contact");
            System.out.println("2. View Contacts");
            System.out.println("3. Search Contact");
            System.out.println("4. Remove Contact");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");

            String choice = sc.nextLine();

            switch (choice) {
                case "1":
                    addContact();
                    break;

                case "2":
                    viewContacts();
                    break;

                case "3":
                    searchContact();
                    break;

                case "4":
                    removeContact();
                    break;

                case "5":
                    System.out.println("Thank you!");
                    return;

                default:
                    System.out.println("Invalid choice!");
            }
        }
    }
}
