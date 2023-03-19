# this is example

from tkinter import *
from tkinter import ttk
from dataBaseConnection import DBConnection
root = Tk()
root.geometry("400x400")
root.minsize(400, 400)
root.maxsize(400, 400)
root.title("Network Anomaly Detector")
obj = DBConnection()
#global loginFrame, registerFrame 
#global registerFrame 


def home():
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    loginBtn = ttk.Button(mainframe, text="Login", padding=20, command=lambda: Login(0))
    registerBtn = ttk.Button(mainframe, text="Register", padding=20,command=Register)
    loginBtn.grid(row=0, column=1, sticky=W)
    ttk.Label(mainframe, text="             ", padding=20).grid(row=0, column=2)
    registerBtn.grid(row=0, column=3, sticky=E)


def Login(status):
    loginFrame = ttk.Frame(root, padding="3 3 12 12")
    loginFrame.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    if(status == 2):
        ttk.Label(loginFrame, text="successfully registered", padding=10).pack()
        ttk.Label(loginFrame,text="Please login to continue").pack()
    else:
        ttk.Label(loginFrame,text="Clicked the Login button").pack()
    ttk.Button(loginFrame, text="Home", command=home).pack()
    
    return

def rSubmit(email, usr, passw,rf):
    emailErr = ttk.Label(rf, text="Account with the same email already exists.", foreground="red")
    userErr = ttk.Label(rf, text="Account with the same user name already exists.", foreground="red")
    emailErr.forget()
    userErr.forget()
    if(obj.isThere(email, usr) == 0):
        obj.insert(email, usr, passw)
        Login(2)
    elif (obj.isThere(email, usr) == 1):
        emailErr.grid(row=2, column=1, columnspan=3)
    else:
        userErr.grid(row=4, column=1, columnspan=3)
    return

def Register():
    registerFrame = ttk.Frame(root, padding="3 3 12 12")
    registerFrame.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    registerFrame.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    ttk.Label(registerFrame,text="Clicked register button").grid(row=0, column=0, columnspan=4)
    ttk.Label(registerFrame, text="Email ID:", padding=10).grid(row=1, column=0)
    registerEmail = ttk.Entry(registerFrame, width=30)
    registerEmail.grid(row=1, column=1)
    ttk.Label(registerFrame, text="User Name:", padding=10).grid(row=3, column=0)
    registerName = ttk.Entry(registerFrame, width=30)
    registerName.grid(row=3, column=1)
    ttk.Label(registerFrame, text="Password:", padding=10).grid(row=5, column=0)
    registerPass = ttk.Entry(registerFrame, width=30)
    registerPass.grid(row=5, column=1)
    ttk.Button(registerFrame, text="Home", command=home).grid(row=7, column=0)
    ttk.Button(registerFrame, text="Submit", command=lambda : rSubmit(registerEmail.get(), registerName.get(), registerPass.get(), registerFrame)).grid(row=6, column=0)
    return



home()
root.mainloop()
