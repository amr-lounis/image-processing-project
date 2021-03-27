from PIL import ImageTk, Image
from tkinter import filedialog

import functions as fn
import tkinter as tk

def getPath():
    filename = filedialog.askopenfilename()
    print("selected file : ",filename)
    v_path.delete(0,"end")
    v_path.insert(0, filename)
    print("selected file in entry ",v_pathVar.get())
    
    showimg(v_pathVar.get())
    
def showimg(filename):
    try:
        img = Image.open(filename)
        
        # img = fn.Histogram_Image(img)
        
        img = ImageTk.PhotoImage(img)
        w, h = img.width(), img.height()
        
        v_canvas.image = img
        v_canvas.config(width=w, height=h)
        v_canvas.create_image(0, 0, image=img, anchor=tk.NW)
    except:
        print("error show image")
    
root = tk.Tk()
root.geometry("800x600+300+50")
root.title('iris recognition ')

v_bt_path1= tk.Button(root,text="select image")
v_bt_path1.grid(row=0,column=0)
v_bt_path1.config(command = lambda : getPath()  )

v_pathVar = tk.StringVar(root)
v_path = tk.Entry(root,textvariable=v_pathVar,width=100)
v_path.bind("<Return>", lambda x: showimg(v_pathVar.get()))
v_path.grid(row=0,column=1,columnspan=8)

v_canvas=tk.Canvas(root, width=300, height=200, background='white')
v_canvas.grid(row=1,column=0,columnspan=10)
# v_canvas.pack()

root.mainloop()
