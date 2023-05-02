from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import mimetypes
from dataBaseConnection import DBConnection
from datetime import datetime
import os



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

class application:
    def __init__(self, name, root) -> None:
        self.username = name
        # print(f"Hello {self.username}")
        self.filename = None
        self.root = root
        self.idList = []
        self.db = DBConnection()
        
    
    def welcome(self):
        self.frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        ttk.Label(self.frame, text=f"Welcome to Network anomaly detector {self.username}").grid(row=0, column=1, columnspan=4,padx=20, pady=20)
        ttk.Button(self.frame,text="Detect Anomaly", command=self.detectAnomaly).grid(row=2, column=0,padx=20, pady=20)
        ttk.Button(self.frame, text="Show Results", command=self.showResults).grid(row=3, column=0, padx=20, pady=20)
        # ttk.Button(self.frame,text="Back").grid(row=0, column=0)
        # ttk.Button(self.frame,text="Next").grid(row=0, column=6)
    
    def detectAnomaly(self):
        self.frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        ttk.Label(self.frame, text="Select a model.", padding=3).grid(row=0, column=0, columnspan=3)
        ttk.Button(self.frame, text="Decision Tree", padding=2, command=lambda: self.chooseMetrics(1)).grid(row=1, column=0,padx=20, pady=20)
        ttk.Button(self.frame, text="Nearest Centroid", padding=2, command=lambda: self.chooseMetrics(2)).grid(row=3, column=0,padx=20, pady=20)
        ttk.Button(self.frame, text="model 3", padding=2, command=lambda: self.chooseMetrics("model 3")).grid(row=5, column=0,padx=20, pady=20)
        return
    
    def openResults(self, id):
        self.frame = ttk.Frame(self.root, padding= "3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        ttk.Button(self.frame, text="GO BACK", command=self.showResults).grid(row=0, column=0)
        canvas = tk.Canvas(self.frame)
        canvas.grid(row=2, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.grid(row=2, column=1, sticky="ns")

        canvas.config(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas with a grid layout
        frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")
        res= self.db.getResultItemOnId(self.username, id)
        print(id)
        
        x = 0
        for i in res:
            showResults = f'Metric Chosen : {i["Metric_Chosen"]}\nDOS Attack = {i["DoS"]}\nBrute Force Attack = {i["Bruteforce"]}\nPort Scan Attack = {i["Portscan"]}\nBotnet Attack = {i["Botnet"]}\nWeb Attack = {i["Webattack"]}\nInfiltration = {i["Infiltration"]}'
            # label = ttk.Label(frame, text=f'Anomalies Detected are: {i["Anomalies_Detected"]}')
            label = ttk.Label(frame, text=showResults)
            label.grid(row=x, column=0, padx=10, pady=10)
            x = x + 1

    def showResults(self):
        self.frame = ttk.Frame(self.root, padding= "3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        ttk.Button(self.frame, text="Home", command=self.welcome).grid(row = 0, column=1)
        ttk.Label(self.frame, text="Select a result.", padding=3).grid(row=0, column=0, columnspan=3)
        search_entry = tk.Entry(self.frame, width=50)
        search_entry.grid(row=1, column=0, columnspan=4)
        flag = 0
        dates = ""
        res = self.db.getResultItems(self.username)
        def search_action():
            res = self.db.getResultItems(self.username)
            dates = search_entry.get()
            dates = dates + ' 00:00:00' 
            
            canvas = tk.Canvas(self.frame)
            canvas.grid(row=2, column=0, columnspan=8,sticky="nsew")
            
            scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollbar.grid(row=2, column=1, sticky="ns")
            
            canvas.config(yscrollcommand=scrollbar.set)
            canvas.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))
            
            # Create a frame inside the canvas with a grid layout
            frame = ttk.Frame(canvas)
            canvas.create_window((0, 0), window=frame, anchor="nw")
            
            t = 0
            for i in res:
                
                user_date = i["date"].strftime("%Y-%m-%d %H:%M:%S")
                if(user_date == dates):
                    label = ttk.Label(frame, text=f'{i["_id"]}\n{i["date"]}\n{i["filename"]}')
                    label.grid(row=t, column=0, padx=10, pady=10)
                    print(i['_id'])
                    ttk.Button(frame, text="View", command=lambda id=i['_id']:self.openResults(id)).grid(row=t, column=1)
                    t = t + 1
                else:
                    print("error")
            nonlocal flag 
            flag = 1
        
        search_button = ttk.Button(self.frame, text="Search", command=search_action)
        search_button.grid(row=1, column=4)

        if(flag == 0):
            canvas = tk.Canvas(self.frame)
            canvas.grid(row=2, column=0, sticky="nsew")

            scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollbar.grid(row=2, column=1, sticky="ns")

            canvas.config(yscrollcommand=scrollbar.set)
            canvas.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

            # Create a frame inside the canvas with a grid layout
            frame = ttk.Frame(canvas)
            canvas.create_window((0, 0), window=frame, anchor="nw")
            x = 0
            for i in res:
                filename = i['filename'].split('/')[-1]
                label = ttk.Label(frame, text=f'{i["_id"]}\n{i["date"]}\n{filename}')
                label.grid(row=x, column=0, padx=10, pady=10)
                print(i['_id'])
                ttk.Button(frame, text="View", command=lambda id=i['_id']:self.openResults(id)).grid(row=x, column=1)
                x = x + 1

        # for i in res:
        #     label = ttk.Label(frame, text=f'{i["_id"]}\n{i["date"]}\n{["filename"]}')
        #     label.grid(row=x, column=0, padx=10, pady=10)
        #     #print(i['_id'])
        #     ttk.Button(frame, text="View", command=lambda: self.openResults(i["_id"])).grid(row=x, column=1)
        #     x = x + 1
        # ttk.Label(resultFrame, text="res1").grid(row=1, column=0)
        # ttk.Label(resultFrame, text="res2").grid(row=2, column=0)
        # ttk.Label(resultFrame, text="res3").grid(row=3, column=0)
        # ttk.Label(resultFrame, text="res1").grid(row=4, column=0)
        # ttk.Label(resultFrame, text="res2").grid(row=5, column=0)
        # ttk.Label(resultFrame, text="res3").grid(row=6, column=0)
        # ttk.Label(resultFrame, text="res1").grid(row=7, column=0)
        # ttk.Label(resultFrame, text="res2").grid(row=8, column=0)
        # ttk.Label(resultFrame, text="res3").grid(row=9, column=0)
        return
    
    
    def chooseMetrics(self, modelNum):
        self.frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        ttk.Label(self.frame, text="Select a metrics", padding=3).grid(row=0, column=0, columnspan=3)
        ttk.Button(self.frame, text="Precision", padding=2, command=lambda: self.chooseFile(modelNum, 1)).grid(row=1, column=0,padx=20, pady=20)
        ttk.Button(self.frame, text="Recall", padding=2, command=lambda: self.chooseFile(modelNum, 2)).grid(row=3, column=0,padx=20, pady=20)
        ttk.Button(self.frame, text="F1-Score", padding=2, command=lambda: self.chooseFile(modelNum, 3)).grid(row=5, column=0,padx=20, pady=20)
        ttk.Button(self.frame, text="Receiver Operating Characteristic AUC", padding=2, command=lambda: self.chooseFile(modelNum, 4)).grid(row=6, column=0,padx=20, pady=20)
        return
    
    def func(self, button, modelNum, metricNum, frame):
        self.filename =  filedialog.askopenfilename(initialdir = "/home/bhuvan",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        try:
            fileType, encoding = mimetypes.guess_type(self.filename)
            if len(self.filename) == 0:
                messagebox.showerror("Error", "Please select the file")
            else:
                button.config(state="normal")
                button.config(command=lambda file=self.filename, modelNum=modelNum, metricNum=metricNum : self.something(file, modelNum, metricNum, frame))
                print(f"{self.filename} file type is {fileType}")
                # self.fileContents = tk.Text(self.frame, background="green", foreground="white")
                # with open(self.filename, "r") as f:
                #     fc = f.readlines()
                # firstFewLines = fc[:10]

                # self.fileContents.insert("1.0", "\n".join(firstFewLines))
                # ttk.Label(self.frame, text="Here are the contents of the selected file").grid(row=4, column=0, padx=5)
                # self.fileContents.grid(row=5, column=0, padx=5, pady=5)
            
        except TypeError:
            # messagebox.showinfo("error", "Please select the file")
            messagebox.showerror("Error", "Please select a file")
        
    def something(self, file, modelNum, metricNum, frame):
        print(file)
        os.system(f'python3 analysis.py {self.username} {file} {modelNum} {metricNum}')
        ttk.Button(frame, text="Go To Home", command=self.welcome).grid(row=10, column=0)

    def chooseFile(self, modelNum, metricNum):
        self.frame = ttk.Frame(self.root, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.labFrame = ttk.Labelframe(self.frame, text="Browse the input file")
        self.labFrame.grid(row=0, column=0, padx=20, pady=20)
        processButton = ttk.Button(self.frame, text="Start the process", state="disabled", command=lambda file=self.filename, modelNum=modelNum, metricNum=metricNum : self.something(file, modelNum, metricNum, self.frame))

        ttk.Button(self.labFrame, text="choose file", command=lambda: self.func(processButton, modelNum, metricNum, self.frame)).grid(row=1, column=0,padx=20, pady=20)
        processButton.grid(row=3, column=0,padx=20, pady=20)
        # ttk.Label(self.frame, text="Choose a file", padding=3).grid(row=0, column=0, columnspan=3)
        # ttk.Label(self.frame, text="selected this file")
        # filename = "x"
        # ttk.Button(self.frame, text="choose file", command=lambda: self.func(filename)).grid(row=1, column=0)
        # #self.frame.filename =  filedialog.askopenfilename(initialdir = "/home/bhuvan",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        # print(filename)
        return

    