import tkinter as tk

Username = "Luffy"
root = tk.Tk()

# create a container frame
container = tk.Frame(root)
container.grid(row=0, column=0, sticky="nsew")

# create multiple frames
frame1 = tk.Frame(container, bg="red")
frame1.grid(row=0, column=0, sticky="nsew")

frame2 = tk.Frame(container, bg="green")
frame2.grid(row=0, column=0, sticky="nsew")

frame3 = tk.Frame(container, bg="blue")
frame3.grid(row=0, column=0, sticky="nsew")

# add some widgets to the frames
label1 = tk.Label(frame1, text=f"This is frame 1 {Username}")
label1.grid(row=0, column=0)

button1 = tk.Button(frame1, text="Go to frame 2", command=frame2.tkraise)
button1.grid(row=1, column=0)

label2 = tk.Label(frame2, text="This is frame 2")
label2.grid(row=0, column=0)

button2 = tk.Button(frame2, text="Go to frame 3", command=frame3.tkraise)
button2.grid(row=1, column=0)

label3 = tk.Label(frame3, text="This is frame 3")
label3.grid(row=0, column=0)

button3 = tk.Button(frame3, text="Go to frame 1", command=frame1.tkraise)
button3.grid(row=1, column=0)

# show the first frame by default
frame1.tkraise()

# create navigation buttons
nav_frame = tk.Frame(root)
nav_frame.grid(row=1, column=0)

button_prev = tk.Button(nav_frame, text="< Prev", command=frame1.tkraise)
button_prev.pack(side="left")

button_next = tk.Button(nav_frame, text="Next >", command=frame2.tkraise)
button_next.pack(side="right")

root.mainloop()

