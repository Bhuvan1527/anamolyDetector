from tkinter import *
from tkinter import ttk

class application:
    def __init__(self, name) -> None:
        self.username = name
        # print(f"Hello {self.username}")
        self.root = Tk()
        self.root.geometry("800x800")
        self.root.minsize(800, 800)
        self.root.maxsize(800, 800)
        self.root.title("Network Anomaly Detector")
        Label(self.root, text=f"Welcome to Network anomaly detector {self.username}").pack()
        self.root.mainloop()
