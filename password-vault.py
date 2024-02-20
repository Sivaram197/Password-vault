import sqlite3
import hashlib
from tkinter import *
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import requests
from io import BytesIO

# Initiating db
with sqlite3.connect("vault.db") as db:
    cursor = db.cursor()

# Creating a table in the database
cursor.execute("""
CREATE TABLE IF NOT EXISTS locker(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);              
""")

# Creating a table for passwords
cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT,
password TEXT NOT NULL);              
""")

window = Tk()
window.title("Secret vault for passwords")

# Fetch and create PhotoImage objects from online images
def fetch_image(url, width, height, background_color):
    response = requests.get(url)
    image_data = BytesIO(response.content)
    lock_icon = Image.open(image_data).resize((width, height))

    # Create a new image with an alpha channel
    background = Image.new("RGBA", lock_icon.size, background_color + (0,))

    # Paste the lock icon onto the new image without using a mask
    background.paste(lock_icon, (0, 0))

    # Convert to RGB mode to remove alpha channel
    background = background.convert("RGB")

    return ImageTk.PhotoImage(background)

# URLs for locked and unlocked lock icons
locked_icon_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRK0uZfY1mnglM4RM2yCr6PENWKbLk9gdhm0Q&usqp=CAU"
unlocked_icon_url = "https://us.123rf.com/450wm/arhimicrostok/arhimicrostok1707/arhimicrostok170703704/81657248-unlock-icon-flat-design-style-validation-of-the-user-completed.jpg?ver=6"

# Dimensions for icons
locked_icon_width, locked_icon_height = 50, 50
unlocked_icon_width, unlocked_icon_height = 80, 80

# Background color
background_color = (255, 255, 255)

# Fetch icons and set initial locked icon
locked_icon = fetch_image(locked_icon_url, locked_icon_width, locked_icon_height, background_color)
unlocked_icon = fetch_image(unlocked_icon_url, unlocked_icon_width, unlocked_icon_height, background_color)

# Create a label to display the lock icon
lock_label = Label(window, image=locked_icon)
lock_label.pack(pady=10)

def update_lock_icon(is_locked=True):
    if is_locked:
        lock_label.config(image=locked_icon)
    else:
        lock_label.config(image=unlocked_icon)

def hashPassword(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()
    return hash

def mainScreen():
    window.geometry("400x200")

    lbl = Label(window, text="Create a master password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show="*")
    txt.pack()
    txt.focus()

    lbl2 = Label(window, text="Re-enter password")
    lbl2.pack()

    txt2 = Entry(window, width=20, show="*")
    txt2.pack()
    txt2.focus()

    lbl3 = Label(window)
    lbl3.pack()

    def savePassword():
        if txt.get() == txt2.get():
            hashedPassword = hashPassword(txt.get().encode('utf-8'))

            updatedPassword = """INSERT INTO locker(password)
            VALUES(?) """
            cursor.execute(updatedPassword, [(hashedPassword)])
            db.commit()

            passVault()
        else:
            lbl3.config(text="ERROR CODE: Passwords do not match")

    btn = Button(window, text="Save", command=savePassword)
    btn.pack()

def loginScreen():
    window.geometry("400x200")

    lbl = Label(window, text="Enter the master password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show="*")
    txt.pack()
    txt.focus()

    lbl2 = Label(window)
    lbl2.pack()

    def getMasterPassword():
        checkHashPassword = hashPassword(txt.get().encode('utf-8'))
        cursor.execute("SELECT * FROM locker WHERE id = 1 AND password = ?", [(checkHashPassword)])
        return cursor.fetchall()

    def checkPassword():
        ISmatch = getMasterPassword()

        if ISmatch:
            passVault()
        else:
            txt.delete(0, 'end')
            lbl2.config(text="ERROR CODE: Wrong Password")

    btn = Button(window, text="Submit", command=checkPassword)
    btn.pack(pady=15)

def addPasswordPopup():
    popup = Toplevel(window)
    popup.title("Add Password")

    lbl_website = Label(popup, text="Website:")
    lbl_website.pack()

    entry_website = Entry(popup, width=30)
    entry_website.pack()

    lbl_username = Label(popup, text="Username:")
    lbl_username.pack()

    entry_username = Entry(popup, width=30)
    entry_username.pack()

    lbl_password = Label(popup, text="Password:")
    lbl_password.pack()

    entry_password = Entry(popup, width=30, show="*")
    entry_password.pack()

    def savePassword():
        website = entry_website.get()
        username = entry_username.get()
        password = entry_password.get()

        if website and password:
            insertPassword = """INSERT INTO passwords(website, username, password)
            VALUES(?, ?, ?)"""
            cursor.execute(insertPassword, (website, username, password))
            db.commit()

            messagebox.showinfo("Success", "Password added successfully")
            popup.destroy()
            passVault()  # Refresh the vault after adding a password
        else:
            messagebox.showerror("Error", "Website and password are required fields")

    btn_save = Button(popup, text="Save", command=savePassword)
    btn_save.pack()

def removePasswordPopup():
    popup = Toplevel(window)
    popup.title("Remove Password")

    lbl_select = Label(popup, text="Select a password to remove:")
    lbl_select.pack()

    password_listbox = Listbox(popup, selectmode=SINGLE, exportselection=False)
    password_listbox.pack()

    # Fetch passwords from the database and populate the listbox
    cursor.execute("SELECT website FROM passwords")
    passwords = cursor.fetchall()
    for password in passwords:
        password_listbox.insert(END, password[0])

    def removePassword():
        selected_index = password_listbox.curselection()
        if selected_index:
            selected_website = password_listbox.get(selected_index)
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to remove the password for {selected_website}?")
            if confirm:
                deletePassword = "DELETE FROM passwords WHERE website = ?"
                cursor.execute(deletePassword, (selected_website,))
                db.commit()

                messagebox.showinfo("Success", "Password removed successfully")
                popup.destroy()
                passVault()  # Refresh the vault after removing a password
        else:
            messagebox.showerror("Error", "Please select a password to remove")

    btn_remove = Button(popup, text="Remove", command=removePassword)
    btn_remove.pack()

def passVault():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("800x600")

    lbl = Label(window, text="Secret Vault", font=("Helvetica", 20))
    lbl.pack(pady=10)

    lb2 = Label(window, image=unlocked_icon)
    lb2.pack()

    # Retrieve existing passwords from the database
    cursor.execute("SELECT * FROM passwords")
    password_records = cursor.fetchall()

    # Display existing passwords in the vault window
    for record in password_records:
        website_label = Label(window, text=f"Website: {record[1]}", font=("Helvetica", 14, "bold"))
        website_label.pack()

        username_label = Label(window, text=f"Username: {record[2]}", font=("Helvetica", 12))
        username_label.pack()

        password_label = Label(window, text=f"Password: {record[3]}", font=("Helvetica", 12))  # Display the original password
        password_label.pack()

        separator = Frame(window, height=2, bd=1, relief=SUNKEN)
        separator.pack(fill=X, padx=5, pady=5)

    add_button = Button(window, text="Add Password", command=addPasswordPopup, font=("Helvetica", 12))
    add_button.pack(pady=10)

    remove_button = Button(window, text="Remove Password", command=removePasswordPopup, font=("Helvetica", 12))
    remove_button.pack(pady=10)

# Check if there is a master password in the locker
cursor.execute("SELECT * FROM locker")
if cursor.fetchall():
    loginScreen()
else:
    mainScreen()

window.mainloop()
