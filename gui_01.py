import tkinter as tk
from PIL import ImageTk, Image
import functions as fn
 
def insertfiles():
    filses= fn.Files("./images/",".bmp")
    for filename in filses:
        lst.insert(tk.END, filename)
 
def showimg(event):
    n = lst.curselection()
    filename = lst.get(n)
    img = Image.open(filename)
    
    # img = fn.Histogram_Image(img)
    
    img = ImageTk.PhotoImage(img)
    w, h = img.width(), img.height()
    print(filename)
    
    canvas.image = img
    canvas.config(width=w, height=h)
    canvas.create_image(5, 0, image=img, anchor=tk.NW)
 
 
root = tk.Tk()
root.geometry("800x600+300+50")
root.title('iris recognition ')

# v_label = tk.Label(root,text= "path")
# v_label.grid(row=0,column=0,padx=10,pady=10)

lst = tk.Listbox(root, width=40)
# lst.grid(0,0)
lst.pack(side="left", fill=tk.BOTH, expand=0)
lst.bind("<<ListboxSelect>>", showimg)
insertfiles()
canvas = tk.Canvas(root)
canvas.pack()
 
root.mainloop()