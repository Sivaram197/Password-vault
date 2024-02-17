# Import necessary files 
import sqlite3, hashlib
from tkinter import * 
from tkinter import simpledialog
from functools import partial
from PIL import Image, ImageTk, ImageDraw 
import requests
from io import BytesIO


# URL for a locked lock icon
locked_icon_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRK0uZfY1mnglM4RM2yCr6PENWKbLk9gdhm0Q&usqp=CAU" 

# URL for an unlocked lock icon
unlocked_icon_url = "https://us.123rf.com/450wm/arhimicrostok/arhimicrostok1707/arhimicrostok170703704/81657248-unlock-icon-flat-design-style-validation-of-the-user-completed.jpg?ver=6"  


#managing the database

#initiating db
with  sqlite3.connect("vault.db") as db:
    #to control the db 
    cursor = db.cursor()

# Creating a table in the database 
cursor.execute("""
CREATE TABLE IF NOT EXISTS locker(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);              
""")



#setting up window
window = Tk()   

window.title("Secret vault for passwords")

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
    lbl2.focus()

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
            cursor.execute(updatedPassword,[(hashedPassword)])
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
    lbl.pack()

    def getMasterPassword():
        checkHashPassword = hashPassword(txt.get().encode('utf-8'))
        cursor.execute("SELECT * FROM locker WHERE id = 1 AND password = ?",[(checkHashPassword)])
        print(checkHashPassword)
        return cursor.fetchall()

    def checkPassword():
        ISmatch = getMasterPassword()

        print(ISmatch)
        if ISmatch:
            passVault()
        else:
            txt.delete(0, 'end') 
            lbl.config(text="ERROR CODE: Wrong Password")


    btn = Button(window, text="Submit", command=checkPassword)
    btn.pack(pady=15) 


background_color = (255, 255, 255)

# Function to fetch and create PhotoImage objects from online images
def fetch_image(url,width,height,background_color):
    response = requests.get(url)
    image_data = BytesIO(response.content)
    lock_icon = Image.open(image_data).resize((width, height))

    # Create a new transparent image with the desired background color
    background = Image.new("RGB", lock_icon.size, (0, 0, 0, 0))
    background.paste(lock_icon, (0, 0))

    # Convert to RGB mode to remove alpha channel
    background = background.convert("RGB")

    return ImageTk.PhotoImage(background)

locked_icon_width, locked_icon_height = 50, 50  
unlocked_icon_width, unlocked_icon_height = 80, 80


locked_icon = fetch_image(locked_icon_url, locked_icon_width, locked_icon_height,background_color)
unlocked_icon = fetch_image(unlocked_icon_url, unlocked_icon_width, unlocked_icon_height,background_color)

# Create a label to display the lock icon
lock_label = Label(window, image=locked_icon)
lock_label.pack(pady=10)

def passVault():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("700x450")

    lb2 = Label(window,image=unlocked_icon)
    lb2.config(anchor=CENTER)
    lb2.pack()

    lbl = Label(window, text="Secret Vault")
    lbl.config(anchor=CENTER)
    lbl.pack()

def update_lock_icon(is_locked=True):
    if is_locked:
        lock_label.config(image=locked_icon)
    else:
        lock_label.config(image=unlocked_icon)



cursor.execute("SELECT * FROM locker")

if cursor.fetchall():
    loginScreen()
else :
    mainScreen()    
window.mainloop()