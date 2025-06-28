import hashlib
import datetime

# In-memory user data for simplicity (you can extend to file/database)
users = {}
logged_in_user = None

# Hashing function for password security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Utility for timestamp
def current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

# User Signup
def signup():
    global users
    username = input("Enter username (3-20 chars): ")
    if not (3 <= len(username) <= 20 and username.isalnum()):
        print("Username must be 3–20 alphanumeric characters.")
        return
    password = input("Enter password (6-20 chars): ")
    if not (6 <= len(password) <= 20):
        print("Password must be 6–20 characters.")
        return
    users[username] = hash_password(password)
    print("Signup successful.")

# User Login
def login():
    global logged_in_user
    username = input("Username: ")
    password = input("Password: ")
    if username in users and users[username] == hash_password(password):
        logged_in_user = username
        print(f"Welcome, {username}!")
    else:
        print("Invalid username or password.")

# Glucose Entry
def add_glucose():
    try:
        glucose = float(input("Enter glucose level (mg/dL): "))
        if not 20 <= glucose <= 600:
            raise ValueError("Glucose level must be between 20 and 600 mg/dL.")
        timestamp = current_time()
        with open(f"{logged_in_user}_glucose.txt", "a") as file:
            file.write(f"{timestamp}: {glucose} mg/dL\n")
        if glucose < 70:
            print("⚠️ Hypoglycemia Alert: Seek medical attention!")
        elif glucose > 180:
            print("⚠️ Hyperglycemia Alert: Take necessary precautions!")
        else:
            print("✅ Glucose level recorded.")
    except ValueError as ve:
        print(f"Error: {ve}")

# Insulin Dose Calculator
def calculate_insulin():
    try:
        glucose = float(input("Enter glucose level for insulin suggestion: "))
        if glucose > 180:
            dose = (glucose - 100) / 50
            print(f"💉 Recommended insulin dose: {dose:.1f} units")
        else:
            print("No insulin dose needed for glucose ≤ 180 mg/dL.")
    except ValueError:
        print("Glucose level must be a number.")

# Meal Logging
def log_meal():
    try:
        description = input("Meal description: ")
        if not description or len(description) > 200:
            raise ValueError("Meal description must be non-empty and less than 200 characters.")
        carbs = float(input("Carbohydrate intake (g): "))
        if not 0 <= carbs <= 500:
            raise ValueError("Carbohydrate intake must be between 0 and 500 grams.")
        timestamp = current_time()
        with open(f"{logged_in_user}_meals.txt", "a") as file:
            file.write(f"{timestamp}: {description} - {carbs}g carbs\n")
        print("✅ Meal logged successfully.")
    except ValueError as ve:
        print(f"Error: {ve}")

# View Data
def view_data():
    try:
        print("\n📊 Glucose Readings:")
        with open(f"{logged_in_user}_glucose.txt") as gfile:
            print(gfile.read())
    except FileNotFoundError:
        print("No glucose data found.")
    try:
        print("🍽️ Meal Logs:")
        with open(f"{logged_in_user}_meals.txt") as mfile:
            print(mfile.read())
    except FileNotFoundError:
        print("No meal data found.")

# Main Menu after login
def main_menu():
    while True:
        print("\n===== Main Menu =====")
        print("1. Add Glucose Reading")
        print("2. Calculate Insulin Dose")
        print("3. Log Meal")
        print("4. View History")
        print("5. Logout")
        choice = input("Choose an option: ")
        if choice == "1":
            add_glucose()
        elif choice == "2":
            calculate_insulin()
        elif choice == "3":
            log_meal()
        elif choice == "4":
            view_data()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

# Starting point
def start():
    while True:
        print("\n📌 Diabetes Management System")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        option = input("Choose an option: ")
        if option == "1":
            login()
            if logged_in_user:
                main_menu()
        elif option == "2":
            signup()
        elif option == "3":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option.")

# Run the system
start()