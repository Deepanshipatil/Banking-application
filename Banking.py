import mysql.connector
import random
import re
from getpass import getpass

# Database setup
def setup_database():
    conn = mysql.connect('banking_system.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        account_number TEXT UNIQUE NOT NULL,
        dob TEXT NOT NULL,
        city TEXT NOT NULL,
        password TEXT NOT NULL,
        balance REAL NOT NULL,
        contact_number TEXT NOT NULL,
        email TEXT NOT NULL,
        address TEXT NOT NULL,
        is_active INTEGER DEFAULT 1
    )''')

    # Transactions table
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number TEXT NOT NULL,
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_number) REFERENCES users (account_number)
    )''')

    conn.commit()
    conn.close()

# Validation functions
def validate_name(name):
    return bool(re.match(r'^[A-Za-z\s]+$', name))

def validate_contact_number(contact):
    return bool(re.match(r'^\d{10}$', contact))

def validate_email(email):
    return bool(re.match(r'^[\w\.]+@[\w]+\.[a-z]{2,3}$', email))

def validate_password(password):
    return len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isupper() for char in password)

def generate_account_number():
    return str(random.randint(10*9, 10*10 - 1))

# Core functions
def add_user():
    print("\n--- Add User ---")
    name = input("Enter name: ")
    while not validate_name(name):
        print("Invalid name. Please enter again.")
        name = input("Enter name: ")

    dob = input("Enter Date of Birth (YYYY-MM-DD): ")
    city = input("Enter city: ")
    password = getpass("Enter password (min 8 chars, 1 digit, 1 uppercase): ")
    while not validate_password(password):
        print("Invalid password. Please enter again.")
        password = getpass("Enter password (min 8 chars, 1 digit, 1 uppercase): ")

    initial_balance = float(input("Enter initial balance (min 2000): "))
    while initial_balance < 2000:
        print("Minimum balance should be 2000.")
        initial_balance = float(input("Enter initial balance (min 2000): "))

    contact_number = input("Enter contact number: ")
    while not validate_contact_number(contact_number):
        print("Invalid contact number. Please enter again.")
        contact_number = input("Enter contact number: ")

    email = input("Enter email: ")
    while not validate_email(email):
        print("Invalid email. Please enter again.")
        email = input("Enter email: ")

    address = input("Enter address: ")

    account_number = generate_account_number()
    
    conn = sqlite3.connect('banking_system.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO users (name, account_number, dob, city, password, balance, contact_number, email, address)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (name, account_number, dob, city, password, initial_balance, contact_number, email, address))
        conn.commit()
        print(f"User added successfully. Account Number: {account_number}")
    except sqlite3.IntegrityError:
        print("Error: Account could not be created. Try again.")
    finally:
        conn.close()

def show_users():
    print("\n--- User Information ---")
    conn = sqlite3.connect('banking_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, account_number, dob, city, balance, contact_number, email, address, is_active FROM users")
    users = cursor.fetchall()
    conn.close()

    if not users:
        print("No users found.")
        return

    for user in users:
        status = "Active" if user[8] else "Inactive"
        print(f"Name: {user[0]}\nAccount Number: {user[1]}\nDOB: {user[2]}\nCity: {user[3]}\nBalance: {user[4]}\nContact: {user[5]}\nEmail: {user[6]}\nAddress: {user[7]}\nStatus: {status}\n---")

# Main function
def main():
    setup_database()
    
    while True:
        print("\n--- Banking System ---")
        print("1. Add User")
        print("2. Show User")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_user()
        elif choice == "2":
            show_users()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "_main_":
    main()