# Import necessary files 
import sqlite3, hashlib
from tkinter import * 


window = Tk() 

window.title("Secret vault for passwords")

def mainScreen():
    window.geometry("400x250")

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
            pass
        else:
            lbl3.config(text="ERROR CODE: Passwords do not match")
    
    btn = Button(window, text="Save", command=savePassword)
    btn.pack(pady=15)

def loginScreen(): 
    window.geometry("400x250")

    lbl = Label(window, text="Enter the master password")
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show="*")
    txt.pack()
    txt.focus()

    lbl2 = Label(window)
    lbl.pack()

    def checkPassword():
        print("test")

        password = "test"

        if password == txt.get():
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



mainScreen()
window.mainloop()