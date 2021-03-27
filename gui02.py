import tkinter as tk
 
class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.mem = {}
 
    def label(self, text, r, c):
        "Creates a label with a text and row and column as arguments"
        self.label = tk.Label(
            self.root,
            text=text)
        self.label.grid(row=r, column=c)
        return self.label
 
    def entry(self, r, c):
        "Creates an input entry for the user"
        self.v = tk.StringVar()
        self.e = tk.Entry(
            self.root,
            textvariable=self.v)
        self.e.grid(row=r, column=c)
        return self.e
 
    def memorize(self, data):
        self.mem[data] = self.v.get()
        print(self.mem)
 
 
def number_of_students():
    "Creates the input of number of students"
    label = w.label("Number of stundents", 0, 0)
    entry = w.entry(0, 1)
    entry.bind("<Return>", lambda x: w.memorize(label["text"]))
 
 
w = Window()
number_of_students()
w.root.mainloop()