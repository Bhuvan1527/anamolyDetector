from tkinter import *
from tkinter import ttk
from Registration import RegisterFrame
from Registration import Home
from detector import start
root = Tk()
root.geometry("400x400")
root.minsize(400, 400)
root.maxsize(400, 400)
root.title("Network Anomaly Detector")
#Label(root, text="Hello").pack()
hm = Home(root)
# rg = RegisterFrame(root)
# Button(root, text="Login").grid(row=0, column=0)
# Button(root, text="Register", command=rg.display).grid(row=0, column=2)
# Button(root, text="Home", command=hm.display).grid(row=0, column=1)

hm.display()
print("Finished")
root.mainloop()
# start("Shanks")