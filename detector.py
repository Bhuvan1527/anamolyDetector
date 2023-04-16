from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import mimetypes

def lift_prev(container):
    idx = container.winfo_children().index(container.current_frame) - 1
    if idx >= 0:
        container.lift(container.winfo_children()[idx])

def lift_next(container):
    idx = container.winfo_children().index(container.current_frame) + 1
    if idx < len(container.winfo_children()):
        container.lift(container.winfo_children()[idx])


def start(name):
    root = Tk()
    root.geometry("500x500")
    root.minsize(500, 500)
    root.maxsize(500, 500)
    root.title("Network Anomaly Detector")
    container = tk.Frame(root)
    container.grid(row=0, column=0, sticky="nsew")
    application(name, container).welcome()
    root.mainloop()

class application:
    def __init__(self, name, root) -> None:
        self.username = name
        # print(f"Hello {self.username}")
        self.filename = None
        self.root = root
        
    
    def welcome(self):
        self.frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        ttk.Label(self.frame, text=f"Welcome to Network anomaly detector {self.username}").grid(row=0, column=1, columnspan=4,padx=20, pady=20)
        ttk.Button(self.frame,text="Detect Anomaly", command=self.detectAnomaly).grid(row=2, column=0,padx=20, pady=20)
        
        # ttk.Button(self.frame,text="Back").grid(row=0, column=0)
        # ttk.Button(self.frame,text="Next").grid(row=0, column=6)
    
    def detectAnomaly(self):
        self.frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        ttk.Label(self.frame, text="Select a model.", padding=3).grid(row=0, column=0, columnspan=3)
        ttk.Button(self.frame, text="model 1", padding=2, command=lambda: self.chooseMetrics("model 1")).grid(row=1, column=0,padx=20, pady=20)
        ttk.Button(self.frame, text="model 2", padding=2, command=lambda: self.chooseMetrics("model 2")).grid(row=3, column=0,padx=20, pady=20)
        ttk.Button(self.frame, text="model 3", padding=2, command=lambda: self.chooseMetrics("model 3")).grid(row=5, column=0,padx=20, pady=20)
        return
    
    def chooseMetrics(self, modelName):
        self.frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        ttk.Label(self.frame, text="Select a metrics", padding=3).grid(row=0, column=0, columnspan=3)
        ttk.Button(self.frame, text="metric 1", padding=2, command=lambda: self.chooseFile(modelName, "metric 1")).grid(row=1, column=0,padx=20, pady=20)
        ttk.Button(self.frame, text="metric 2", padding=2, command=lambda: self.chooseFile(modelName, "metric 2")).grid(row=3, column=0,padx=20, pady=20)
        ttk.Button(self.frame, text="metric 3", padding=2, command=lambda: self.chooseFile(modelName, "metric 3")).grid(row=5, column=0,padx=20, pady=20)
        return
    
    def func(self, button):
        self.filename =  filedialog.askopenfilename(initialdir = "/home/bhuvan",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        try:
            fileType, encoding = mimetypes.guess_type(self.filename)
            if len(self.filename) == 0:
                messagebox.showerror("Error", "Please select the file")
            else:
                button.config(state="normal")
                print(f"{self.filename} file type is {fileType}")
                self.fileContents = tk.Text(self.frame, background="green", foreground="white")
                with open(self.filename, "r") as f:
                    fc = f.readlines()
                firstFewLines = fc[:10]

                self.fileContents.insert("1.0", "\n".join(firstFewLines))
                ttk.Label(self.frame, text="Here are the contents of the selected file").grid(row=4, column=0, padx=5)
                self.fileContents.grid(row=5, column=0, padx=5, pady=5)
            
        except TypeError:
            # messagebox.showinfo("error", "Please select the file")
            messagebox.showerror("Error", "Please select a file")
        

    def chooseFile(self, modelname, metricname):
        self.frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.labFrame = ttk.Labelframe(self.frame, text="Browse the input file")
        self.labFrame.grid(row=0, column=0, padx=20, pady=20)
        processButton = ttk.Button(self.frame, text="Start the process", state="disabled")

        ttk.Button(self.labFrame, text="choose file", command=lambda: self.func(processButton)).grid(row=1, column=0,padx=20, pady=20)
        processButton.grid(row=3, column=0,padx=20, pady=20)
        # ttk.Label(self.frame, text="Choose a file", padding=3).grid(row=0, column=0, columnspan=3)
        # ttk.Label(self.frame, text="selected this file")
        # filename = "x"
        # ttk.Button(self.frame, text="choose file", command=lambda: self.func(filename)).grid(row=1, column=0)
        # #self.frame.filename =  filedialog.askopenfilename(initialdir = "/home/bhuvan",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        # print(filename)
        return

    