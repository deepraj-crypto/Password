from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email_ = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email_,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data to new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------search----------------------------------- #

def search():
    website = website_entry.get()

    if len(website) == 0:
        messagebox.showinfo(title="Error", message="Please fill in the website detail.")
    else:
        try:
            with open("data.json") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No data file found.")
        else:
            for key in data:
                if key == website:
                    messagebox.showinfo(title="Password",
                                        message=f"Email: {data[key]['email']}\nPassword: {data[key]['password']}")
                elif website not in data:
                    messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=1, column=2)

website_label = Label(text="Website: ")
website_label.grid(row=2, column=1)

email_label = Label(text="Email/Username: ")
email_label.grid(row=3, column=1)

password_label = Label(text="Password: ")
password_label.grid(row=4, column=1)

website_entry = Entry(width=21)
website_entry.grid(row=2, column=2)
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=3, column=2, columnspan=2)
email_entry.insert(0, "deeprajmazumder11@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(row=4, column=2)

password_button = Button(text="Generate Password", highlightthickness=0, command=generate_password)
password_button.grid(row=4, column=3)

add_button = Button(text="Add", highlightthickness=0, width=36, command=save)
add_button.grid(row=5, column=2, columnspan=2)

search_button = Button(text="Search", highlightthickness=0, command=search)
search_button.grid(row=2, column=3)

window.mainloop()
