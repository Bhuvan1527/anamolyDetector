from tkinter import *
from tkinter import ttk
from dataBaseConnection import DBConnection
import re

class Home:
    def __init__(self, root) -> None:
        #self.frame = None
        self.frame = ttk.Frame(root, padding="3 3 12 12")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.RegisterBtn = None
        self.LoginBtn = None
        self.rootWindow = root
    
    def display(self):
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.LoginBtn = ttk.Button(self.frame, text="Login", padding=20, command=lambda: LoginFrame(self.rootWindow).display())
        self.RegisterBtn = ttk.Button(self.frame, text="Register", padding=20,command=lambda: RegisterFrame(self.rootWindow).display())
        self.LoginBtn.grid(row=0, column=1, sticky=W)
        ttk.Label(self.frame, text="             ", padding=20).grid(row=0, column=2)
        self.RegisterBtn.grid(row=0, column=3, sticky=E)

def isEmailCorrect(str) -> bool:
    x = re.search("^[a-zA-Z0-9]+@(gmail.com|uohyd.ac.in)$", str)
    if x is None:
        return False
    else:
        return True

def isUsernameCorrect(str) -> bool:
    x = re.search("^[a-zA-Z_][a-zA-Z0-9_]*$", str)
    if x is None:
        return False
    else:
        return True

    


class LoginFrame:
    def __init__(self, root) -> None: 
        self.frame = ttk.Frame(root, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.username = ttk.Entry(self.frame, justify="left", width=30)
        self.password = ttk.Entry(self.frame, justify="left", width=30)
        self.loginErr = ttk.Label(self.frame, text="Incorrect Username or Password", padding=10, foreground="red")
        self.rootWindow = root
        self.db = DBConnection()
    
    def lsubmit(self):
        un = self.username.get()
        pa = self.password.get()
        self.loginErr.grid_remove()
        if len(un) == 0 or len(pa) == 0:
            self.loginErr = ttk.Label(self.frame, text="Do not leave fields empty", padding=10, foreground="red")
            self.loginErr.grid(row=1, column=1, columnspan=3)
        stat = self.db.Authenticate(un, pa)
        if stat:
            pass
        else:
            self.loginErr = ttk.Label(self.frame, text="Incorrect Username or Password", padding=10, foreground="red")
            self.loginErr.grid(row=1, column=1, columnspan=3)
        return
    
    def display(self) -> None:
        ttk.Label(self.frame, text="Please Login to continue", padding=10).grid(row=0, column=1, columnspan=3)
        ttk.Label(self.frame, text="Username", padding=5).grid(row=2, column=0)
        self.username.grid(row=2, column=1, columnspan=4)
        ttk.Label(self.frame, text="Password", padding=5).grid(row=4, column=0)
        self.password.grid(row=4, column=1, columnspan=4)
        ttk.Button(self.frame, text="Login", width=5, padding=3, command=self.lsubmit).grid(row=6, column=1)
        ttk.Button(self.frame, text="Home", width=5, padding=3, command=lambda:Home(self.rootWindow).display()).grid(row=7, column=1)
        return

class RegisterFrame:
    def __init__(self, root) -> None:
        print("created the object\n")
        #self.frame = None
        self.frame = ttk.Frame(root, padding="3 3 12 12")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.email = None
        self.username = None
        self.password = None
        self.emailErr = ttk.Label(self.frame, text="Account with the same email already exists.", foreground="red")
        self.usernameErr = ttk.Label(self.frame, text="Account with the same user name already exists.", foreground="red")
        self.emailErr1 = ttk.Label(self.frame, text="Invalid Email Address", foreground="red")
        self.registerErr = ttk.Label(self.frame, text="Do not leave the fields empty", foreground="red")
        # self.emailErr = None
        # self.usernameErr = None
        self.rootWindow = root
        self.db = DBConnection()
    
    def rSubmit(self, email, usr, passw):
        self.emailErr.grid_remove()
        self.usernameErr.grid_remove()
        self.emailErr1.grid_remove()
        if len(email) == 0 or len(usr) == 0 or len(passw) == 0:
            self.registerErr.grid(row=1, column=1, columnspan=3)
            return
        if not isEmailCorrect(email):
            #self.emailErr.__setattr__("text", "Invalid Email Address")
            self.emailErr1.grid(row=3, column=1, columnspan=3)
            return
        x = self.db.isThere(email, usr)
        if(x == 0):
            self.db.insert(email, usr, passw)
            LoginFrame(self.rootWindow).display()
            #Login(2)
        elif (x == 1):
            self.emailErr.grid(row=3, column=1, columnspan=3)
        else:
            self.usernameErr.grid(row=5, column=1, columnspan=3)
        return

    def display(self):
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        print("Entered display\n")
        ttk.Label(self.frame,text="Clicked register button").grid(row=0, column=0, columnspan=4)
        ttk.Label(self.frame, text="Email ID:", padding=10).grid(row=2, column=0)
        self.email = ttk.Entry(self.frame, width=30)
        self.email.grid(row=2, column=1)
        ttk.Label(self.frame, text="User Name:", padding=10).grid(row=4, column=0)
        self.username = ttk.Entry(self.frame, width=30)
        self.username.grid(row=4, column=1)
        ttk.Label(self.frame, text="Password:", padding=10).grid(row=6, column=0)
        self.password = ttk.Entry(self.frame, width=30)
        self.password.grid(row=6, column=1)
        ttk.Button(self.frame, text="Home", command=lambda: Home(self.rootWindow).display()).grid(row=8, column=0)
        ttk.Button(self.frame, text="Submit", command=lambda : self.rSubmit(self.email.get(), self.username.get(), self.password.get())).grid(row=7, column=0)