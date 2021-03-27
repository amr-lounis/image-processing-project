import tkinter as tk
import glob
from PIL import ImageTk, Image
import functions as fn

 
def insertfiles():
    for filename in glob.glob("images/*.bmp"):
        lst.insert(tk.END, filename)
 
def showimg(event):
    n = lst.curselection()
    filename = lst.get(n)
    img = Image.open(filename)
    
    img = fn.ContrastInvers(img)
    
    img = ImageTk.PhotoImage(img)
    w, h = img.width(), img.height()
    print(filename)
    canvas.image = img
    canvas.config(width=w, height=h)
    canvas.create_image(0, 0, image=img, anchor=tk.NW)
 
 
root = tk.Tk()
root.geometry("800x600+300+50")
lst = tk.Listbox(root, width=20)
lst.pack(side="left", fill=tk.BOTH, expand=0)
lst.bind("<<ListboxSelect>>", showimg)
insertfiles()
canvas = tk.Canvas(root)
canvas.pack()
 
root.mainloop()