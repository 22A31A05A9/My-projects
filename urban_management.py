import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

current_user = ""
current_role = 0  # To store the current user's role

# Database Setup
conn = sqlite3.connect("Tkinter Python GUIs/user_database.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                  user_id INTEGER PRIMARY KEY,
                  username TEXT NOT NULL UNIQUE,
                  phone TEXT NOT NULL,
                  password TEXT NOT NULL,
                  address TEXT NOT NULL,
                  pincode TEXT NOT NULL,
                  email TEXT NOT NULL,
                  role TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
                  id INTEGER PRIMARY KEY,
                  issue TEXT,
                  location TEXT,
                  user_id INTEGER,
                  FOREIGN KEY (user_id) REFERENCES users(user_id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                  admin_id INTEGER PRIMARY KEY,
                  username TEXT NOT NULL UNIQUE,
                  phone TEXT NOT NULL,
                  password TEXT NOT NULL,
                  address TEXT NOT NULL,
                  pincode TEXT NOT NULL,
                  email TEXT NOT NULL,
                  role TEXT NOT NULL)''')
conn.commit()

# Create the main application window
root = Tk()
root.title("Urban Development Feedback System")
root.geometry("700x500")
root.config(background="black")

# Function to check if a user or admin exists
def user_exists(username, password, role):
    if role == "user":
        cursor.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?", (username, password, role))
    elif role == "admin":
        cursor.execute("SELECT * FROM admins WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    return user is not None

# Function to register a new user
def register_user(username, phone, password, address, pincode, email, role):
    cursor.execute("INSERT INTO users (username, phone, password, address, pincode, email, role) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (username, phone, password, address, pincode, email, role))
    conn.commit()
    user_register_username_entry.delete(0,END)
    user_register_phone_entry.delete(0, END)
    user_register_password_entry.delete(0, END)
    user_register_confirm_password_entry.delete(0, END)
    user_register_address_entry.delete(0, END)
    user_register_pincode_entry.delete(0, END)
    user_register_email_entry.delete(0, END)
    messagebox.showinfo("Success", f"Registration successful as a {role}. You can now log in.")

# Function to register a new admin
def register_admin(username, phone, password, address, pincode, email, role):
    cursor.execute("INSERT INTO admins (username, phone, password, address, pincode, email, role) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (username, phone, password, address, pincode, email, role))
    conn.commit()
    admin_register_username_entry.delete(0,END)
    admin_register_phone_entry.delete(0, END)
    admin_register_password_entry.delete(0, END)
    admin_register_confirm_password_entry.delete(0, END)
    admin_register_address_entry.delete(0, END)
    admin_register_pincode_entry.delete(0, END)
    admin_register_email_entry.delete(0, END)
    messagebox.showinfo("Success", f"Registration successful as a {role}. You can now log in.")

# Function to switch to the login page
def switch_to_login_page():
    global current_user, current_role
    login_frame.grid(row=0, column=0, padx=10, pady=10)
    admin_login_frame.grid_remove()
    user_register_frame.grid_remove()
    admin_register_frame.grid_remove()
    user_feedback_frame.grid_remove()
    admin_feedback_frame.grid_remove()
    user_login_frame.grid_remove()
    current_user = ""
    current_role = ""

# Function to handle user login
def user_login():
    username = user_login_username_entry.get()
    password = user_login_password_entry.get()

    if user_exists(username, password, "user"):
        global current_user, current_role
        current_user = username
        current_role = "user"
        user_login_username_entry.delete(0, END)
        user_login_password_entry.delete(0, END)
        messagebox.showinfo("Success", "User login successful.")
        switch_to_user_feedback_page()
    else:
        messagebox.showerror("Error", "User username or password is incorrect.")
        user_login_username_entry.delete(0, END)
        user_login_password_entry.delete(0, END)

# Function to handle admin login
def admin_login():
    username = admin_login_username_entry.get()
    password = admin_login_password_entry.get()

    if user_exists(username, password, "admin"):  # Corrected to check admin table
        global current_user, current_role
        current_user = username
        current_role = "admin"
        admin_login_username_entry.delete(0, END)
        admin_login_password_entry.delete(0, END)
        messagebox.showinfo("Success", "Admin login successful.")
        switch_to_admin_feedback_page()
    else:
        messagebox.showerror("Error", "Admin username or password is incorrect.")
        admin_login_username_entry.delete(0, END)
        admin_login_password_entry.delete(0, END)


# Function to switch to the user feedback page
def switch_to_user_feedback_page():
    user_feedback_frame.grid(row=0, column=0, padx=10, pady=10)
    login_frame.grid_remove()
    admin_login_frame.grid_remove()
    user_register_frame.grid_remove()
    admin_register_frame.grid_remove()
    admin_feedback_frame.grid_remove()
    user_login_frame.grid_remove()
    fetch_data(current_user)

# Function to switch to the admin feedback page
def switch_to_admin_feedback_page():
    admin_feedback_frame.grid(row=0, column=0, padx=10, pady=10)
    login_frame.grid_remove()
    admin_login_frame.grid_remove()
    user_register_frame.grid_remove()
    admin_register_frame.grid_remove()
    user_feedback_frame.grid_remove()
    user_login_frame.grid_remove()
    fetch_all_feedback_data()

# Function to switch to user login page
def switch_to_user_login_page():
    user_register_frame.grid_remove()
    login_frame.grid_remove()
    admin_login_frame.grid_remove()
    admin_register_frame.grid_remove()
    admin_feedback_frame.grid_remove()
    user_feedback_frame.grid_remove()
    user_login_frame.grid(row=0, column=0, padx=10, pady=10)

# Function to switch to admin login page
def switch_to_admin_login_page():
    user_register_frame.grid_remove()
    login_frame.grid_remove()
    admin_login_frame.grid(row=0, column=0, padx=10, pady=10)
    admin_register_frame.grid_remove()
    admin_feedback_frame.grid_remove()
    user_feedback_frame.grid_remove()
    user_login_frame.grid_remove()



# Function to switch to admin registration page
def switch_to_admin_registration_page():
    admin_register_frame.grid(row=0, column=0, padx=10, pady=10)
    login_frame.grid_remove()
    admin_login_frame.grid_remove()
    user_register_frame.grid_remove()
    user_feedback_frame.grid_remove()
    user_login_frame.grid_remove()
    admin_feedback_frame.grid_remove()

# Function to switch to user registration page
def switch_to_user_registration_page():
    user_register_frame.grid(row=0, column=0, padx=10, pady=10)
    login_frame.grid_remove()
    admin_login_frame.grid_remove()
    admin_register_frame.grid_remove()
    admin_feedback_frame.grid_remove()
    user_feedback_frame.grid_remove()
    user_login_frame.grid_remove()

# Function to log out
def logout():
    global current_user, current_role
    current_user = ""
    current_role = ""
    switch_to_login_page()

# Function to raise an issue
def raise_issue():
    issue = user_issue_entry.get()
    location = user_location_entry.get()

    if issue and location:
        cursor.execute("INSERT INTO feedback (issue, location, user_id) VALUES (?, ?, ?)",
                       (issue, location, get_user_id(current_user)))
        conn.commit()
        user_issue_entry.delete(0, END)
        user_location_entry.delete(0, END)
        messagebox.showinfo("Success", "Issue submitted successfully.")
        fetch_data(current_user)
    else:
        messagebox.showerror("Error", "Please fill in both issue and location fields.")

# Function to retrieve the user ID based on the username
def get_user_id(username):
    cursor.execute("SELECT user_id FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    return user[0] if user else None

# Function to fetch and display data from the database for a user
def fetch_data(user):
    cursor.execute("SELECT * FROM feedback WHERE user_id=?", (get_user_id(user),))
    data = cursor.fetchall()
    user_feedback_text.delete(1.0, END)  # Clear the text widget

    if data:
        for row in data:
            user_feedback_text.insert(END, f"ID: {row[0]}\nIssue: {row[1]}\nLocation: {row[2]}\n\n")
    else:
        user_feedback_text.insert(END, "No data available")

# Function to fetch and display all feedback data for an admin
def fetch_all_feedback_data():
    cursor.execute("SELECT feedback.id, feedback.issue, feedback.location, users.username FROM feedback INNER JOIN users ON feedback.user_id = users.user_id")
    data = cursor.fetchall()
    admin_feedback_text.delete(1.0, END)  # Clear the text widget

    if data:
        for row in data:
            admin_feedback_text.insert(END, f"ID: {row[0]}\nIssue: {row[1]}\nLocation: {row[2]}\nUser: {row[3]}\n\n")
    else:
        admin_feedback_text.insert(END, "No data available")

# Assuming you want your main frame to fill the entire root window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create frames for different pages
login_frame = Frame(root)
user_login_frame=Frame(root)
admin_login_frame = Frame(root)
user_register_frame = Frame(root)
admin_register_frame = Frame(root)
user_feedback_frame = Frame(root)
admin_feedback_frame = Frame(root)

# Grid settings for all frames
for frame in [login_frame, user_login_frame,admin_login_frame, user_register_frame, admin_register_frame, user_feedback_frame, admin_feedback_frame]:
    frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

login_label = Label(login_frame, text="Welcome to Urban Development Feedback System", font=("Helvetica", 14))
login_label.grid(row=0, column=0, columnspan=4, pady=10)

login_user_button = Button(login_frame, text="User", font=("Helvetica", 12), command=lambda: switch_to_user_login_page())
login_user_button.grid(row=1, column=0,columnspan=2, pady=5,padx=5,ipadx=20,ipady=10)

login_admin_button = Button(login_frame, text="Admin", font=("Helvetica", 12), command=lambda: switch_to_admin_login_page())
login_admin_button.grid(row=1, column=2,columnspan=2, pady=5,padx=25,ipadx=20,ipady=10)


# Create widgets for the user registration page
user_register_label = Label(user_register_frame, text="User Registration", font=("Helvetica", 14))
user_register_label.grid(row=0, column=0, columnspan=2, pady=10)

user_register_username_label = Label(user_register_frame, text="Username:", font=("Helvetica", 12))
user_register_username_label.grid(row=1, column=0, pady=5)

user_register_username_entry = Entry(user_register_frame, width=30, font=("Helvetica", 12))
user_register_username_entry.grid(row=1, column=1, pady=5)

user_register_phone_label = Label(user_register_frame, text="Phone Number:", font=("Helvetica", 12))
user_register_phone_label.grid(row=2, column=0, pady=5)

user_register_phone_entry = Entry(user_register_frame, width=30, font=("Helvetica", 12))
user_register_phone_entry.grid(row=2, column=1, pady=5)

user_register_password_label = Label(user_register_frame, text="Password:", font=("Helvetica", 12))
user_register_password_label.grid(row=3, column=0, pady=5)

user_register_password_entry = Entry(user_register_frame, width=30, font=("Helvetica", 12, "bold"), show="*")
user_register_password_entry.grid(row=3, column=1, pady=5)

user_register_confirm_password_label = Label(user_register_frame, text="Confirm Password:", font=("Helvetica", 12))
user_register_confirm_password_label.grid(row=4, column=0, pady=5)

user_register_confirm_password_entry = Entry(user_register_frame, width=30, font=("Helvetica", 12, "bold"), show="*")
user_register_confirm_password_entry.grid(row=4, column=1, pady=5)

user_register_address_label = Label(user_register_frame, text="Address:", font=("Helvetica", 12))
user_register_address_label.grid(row=5, column=0, pady=5)

user_register_address_entry = Entry(user_register_frame, width=30, font=("Helvetica", 12))
user_register_address_entry.grid(row=5, column=1, pady=5)

user_register_pincode_label = Label(user_register_frame, text="Pincode:", font=("Helvetica", 12))
user_register_pincode_label.grid(row=6, column=0, pady=5)

user_register_pincode_entry = Entry(user_register_frame, width=30, font=("Helvetica", 12))
user_register_pincode_entry.grid(row=6, column=1, pady=5)

user_register_email_label = Label(user_register_frame, text="Email:", font=("Helvetica", 12))
user_register_email_label.grid(row=7, column=0, pady=5)

user_register_email_entry = Entry(user_register_frame, width=30, font=("Helvetica", 12))
user_register_email_entry.grid(row=7, column=1, pady=5)

user_register_button = Button(user_register_frame, text="Register", command=lambda: register_user(user_register_username_entry.get(), user_register_phone_entry.get(), user_register_password_entry.get(), user_register_address_entry.get(), user_register_pincode_entry.get(), user_register_email_entry.get(), "user"), font=("Helvetica", 12))
user_register_button.grid(row=8, column=0, columnspan=2, pady=10)

user_register_back_button = Button(user_register_frame, text="HOME", command=switch_to_login_page, font=("Helvetica", 12))
user_register_back_button.grid(row=9, column=0, columnspan=2, pady=5)

# Create widgets for the admin registration page
admin_register_label = Label(admin_register_frame, text="Admin Registration", font=("Helvetica", 14))
admin_register_label.grid(row=0, column=0, columnspan=2, pady=10)

admin_register_username_label = Label(admin_register_frame, text="Username:", font=("Helvetica", 12))
admin_register_username_label.grid(row=1, column=0, pady=5)

admin_register_username_entry = Entry(admin_register_frame, width=30, font=("Helvetica", 12))
admin_register_username_entry.grid(row=1, column=1, pady=5)

admin_register_phone_label = Label(admin_register_frame, text="Phone Number:", font=("Helvetica", 12))
admin_register_phone_label.grid(row=2, column=0, pady=5)

admin_register_phone_entry = Entry(admin_register_frame, width=30, font=("Helvetica", 12))
admin_register_phone_entry.grid(row=2, column=1, pady=5)

admin_register_password_label = Label(admin_register_frame, text="Password:", font=("Helvetica", 12))
admin_register_password_label.grid(row=3, column=0, pady=5)

admin_register_password_entry = Entry(admin_register_frame, width=30, font=("Helvetica", 12, "bold"), show="*")
admin_register_password_entry.grid(row=3, column=1, pady=5)

admin_register_confirm_password_label = Label(admin_register_frame, text="Confirm Password:", font=("Helvetica", 12))
admin_register_confirm_password_label.grid(row=4, column=0, pady=5)

admin_register_confirm_password_entry = Entry(admin_register_frame, width=30, font=("Helvetica", 12, "bold"), show="*")
admin_register_confirm_password_entry.grid(row=4, column=1, pady=5)

admin_register_address_label = Label(admin_register_frame, text="Address:", font=("Helvetica", 12))
admin_register_address_label.grid(row=5, column=0, pady=5)

admin_register_address_entry = Entry(admin_register_frame, width=30, font=("Helvetica", 12))
admin_register_address_entry.grid(row=5, column=1, pady=5)

admin_register_pincode_label = Label(admin_register_frame, text="Pincode:", font=("Helvetica", 12))
admin_register_pincode_label.grid(row=6, column=0, pady=5)

admin_register_pincode_entry = Entry(admin_register_frame, width=30, font=("Helvetica", 12))
admin_register_pincode_entry.grid(row=6, column=1, pady=5)

admin_register_email_label = Label(admin_register_frame, text="Email:", font=("Helvetica", 12))
admin_register_email_label.grid(row=7, column=0, pady=5)

admin_register_email_entry = Entry(admin_register_frame, width=30, font=("Helvetica", 12))
admin_register_email_entry.grid(row=7, column=1, pady=5)

admin_register_button = Button(admin_register_frame, text="Register", command=lambda: register_admin(admin_register_username_entry.get(), admin_register_phone_entry.get(), admin_register_password_entry.get(), admin_register_address_entry.get(), admin_register_pincode_entry.get(), admin_register_email_entry.get(), "admin"), font=("Helvetica", 12))
admin_register_button.grid(row=8, column=0, columnspan=2, pady=10)

admin_register_back_button = Button(admin_register_frame, text="HOME", command=switch_to_login_page, font=("Helvetica", 12))
admin_register_back_button.grid(row=9, column=0, columnspan=2, pady=5)

#User login page
user_login_label = Label(user_login_frame, text="User Login", font=("Helvetica", 14))
user_login_label.grid(row=0, column=0, columnspan=2, pady=10)

user_login_username_label = Label(user_login_frame, text="Username:", font=("Helvetica", 12))
user_login_username_label.grid(row=1, column=0, pady=5)

user_login_username_entry = Entry(user_login_frame, width=30, font=("Helvetica", 12))
user_login_username_entry.grid(row=1, column=1, pady=5)

user_login_password_label = Label(user_login_frame, text="Password:", font=("Helvetica", 12))
user_login_password_label.grid(row=2, column=0, pady=5)

user_login_password_entry = Entry(user_login_frame, width=30, font=("Helvetica", 12, "bold"), show="*")
user_login_password_entry.grid(row=2, column=1, pady=5)

user_login_button = Button(user_login_frame, text="Login", command=user_login, font=("Helvetica", 12))
user_login_button.grid(row=3, column=0, columnspan=2, pady=10)

user_login_register_button = Button(user_login_frame, text="CREATE ACCOUNT", command=switch_to_user_registration_page, font=("Helvetica", 12))
user_login_register_button.grid(row=4, column=0, columnspan=2, pady=5)

user_login_back_button = Button(user_login_frame, text="HOME", command=switch_to_login_page, font=("Helvetica", 12))
user_login_back_button.grid(row=5, column=0, columnspan=2, pady=5)

#Admin login page
admin_login_label = Label(admin_login_frame, text="Admin Login", font=("Helvetica", 14))
admin_login_label.grid(row=0, column=0, columnspan=2, pady=10)

admin_login_username_label = Label(admin_login_frame, text="Username:", font=("Helvetica", 12))
admin_login_username_label.grid(row=1, column=0, pady=5)

admin_login_username_entry = Entry(admin_login_frame, width=30, font=("Helvetica", 12))
admin_login_username_entry.grid(row=1, column=1, pady=5)

admin_login_password_label = Label(admin_login_frame, text="Password:", font=("Helvetica", 12))
admin_login_password_label.grid(row=2, column=0, pady=5)

admin_login_password_entry = Entry(admin_login_frame, width=30, font=("Helvetica", 12, "bold"), show="*")
admin_login_password_entry.grid(row=2, column=1, pady=5)

admin_login_button = Button(admin_login_frame, text="Login", command=admin_login, font=("Helvetica", 12))
admin_login_button.grid(row=3, column=0, columnspan=2, pady=10)

admin_login_register_button = Button(admin_login_frame, text="CREATE ACCOUNT", command=switch_to_admin_registration_page, font=("Helvetica", 12))
admin_login_register_button.grid(row=4, column=0, columnspan=2, pady=5)

admin_login_back_button = Button(admin_login_frame, text="HOME", command=switch_to_login_page, font=("Helvetica", 12))
admin_login_back_button.grid(row=5, column=0, columnspan=2, pady=5)


# Create widgets for the user feedback page
user_feedback_label = Label(user_feedback_frame, text="Raise Issue", font=("Helvetica", 14))
user_feedback_label.grid(row=0, column=0, columnspan=2, pady=10)

user_issue_label = Label(user_feedback_frame, text="Issue:", font=("Helvetica", 12))
user_issue_label.grid(row=1, column=0, pady=5)

user_issue_entry = Entry(user_feedback_frame, width=30, font=("Helvetica", 12))
user_issue_entry.grid(row=1, column=1, pady=5)

user_location_label = Label(user_feedback_frame, text="Location:", font=("Helvetica", 12))
user_location_label.grid(row=2, column=0, pady=5)

user_location_entry = Entry(user_feedback_frame, width=30, font=("Helvetica", 12))
user_location_entry.grid(row=2, column=1, pady=5)

raise_issue_button = Button(user_feedback_frame, text="Raise Issue", command=raise_issue, font=("Helvetica", 12))
raise_issue_button.grid(row=3, column=0, columnspan=2, pady=10)

user_feedback_text = Text(user_feedback_frame, width=50, height=10, font=("Helvetica", 12))
user_feedback_text.grid(row=4, column=0, columnspan=2, pady=10)

user_logout_button = Button(user_feedback_frame, text="Logout", command=logout, font=("Helvetica", 12))
user_logout_button.grid(row=5, column=0, columnspan=2, pady=10)

# Create widgets for the admin feedback page
admin_feedback_label = Label(admin_feedback_frame, text="Feedback from Users", font=("Helvetica", 14))
admin_feedback_label.grid(row=0, column=0, columnspan=2, pady=10)

admin_feedback_text = Text(admin_feedback_frame, width=50, height=10, font=("Helvetica", 12))
admin_feedback_text.grid(row=1, column=0, columnspan=2, pady=10)

admin_logout_button = Button(admin_feedback_frame, text="Logout", command=logout, font=("Helvetica", 12))
admin_logout_button.grid(row=2, column=0, columnspan=2, pady=10)

# Initially show the login page
switch_to_login_page()

# Start the application
root.mainloop()
