# Import necessary files 
import sqlite3, hashlib
from tkinter import * 
from tkinter import simpledialog
from functools import partial

#managing the database

#initiating db
with  sqlite3.connect("pass_valut.db") as db:
    #to control the db 
    cursor = db.cursor()

#creaing a table in the database 
cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);              
""")



#setting up window
window = Tk()   

window.title("Secret vault for passwords")


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

            updatedPassword = """INSERT INTO masterpassword(password)
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
        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?",[(checkHashPassword)])
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

def passVault():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("700x450")

    lbl = Label(window, text="Secret Vault")
    lbl.config(anchor=CENTER)
    lbl.pack()


cursor.execute("SELECT * FROM masterpassword")

if cursor.fetchall():
    loginScreen()
else :
    mainScreen()    
window.mainloop()