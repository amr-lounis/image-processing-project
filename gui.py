from PIL import ImageTk, Image
from tkinter import filedialog

import functions as fn
import tkinter as tk
    
# ----------------------------------------------------
def getPath()-> None:
    filename = filedialog.askopenfilename()
    print("selected file : ",filename)
    v_path_input.delete(0,"end")
    v_path_input.insert(0, filename)
    print("selected file in entry ",v_pathVar_input.get())
    
    Showimg(v_pathVar_input.get())
    
# ----------------------------------------------------
def Showimg(filename):
    try:
        imageIn = Image.open(filename)
        imageIn = fn.ConvertImage_2d(imageIn)
        
        img = ImageTk.PhotoImage(imageIn)
        w, h = img.width(), img.height()
        
        v_canvas_input.image = img
        v_canvas_input.config(width=w, height=h)
        v_canvas_input.create_image(0, 0, image=img, anchor=tk.NW)
    except:
        print("error show image")
# ----------------------------------------------------
def ShowHistogram():
    try:
        filename =v_pathVar_input.get()
        imageIn = Image.open(filename)
        imageIn = fn.ConvertImage_2d(imageIn)
        
        img = fn.Histogram_Image(imageIn)
        
        img = ImageTk.PhotoImage(img)
        w, h = img.width(), img.height()
        
        v_canvas_output.image = img
        v_canvas_output.config(width=w, height=h)
        v_canvas_output.create_image(0, 0, image=img, anchor=tk.NW)
    except:
        print("error show image outout")

def ShowLissage():
    import numpy as np
    try:
        filename =v_pathVar_input.get()
        imageIn = Image.open(filename)
        imageIn = fn.ConvertImage_2d(imageIn)
        
        filter0 = np.array([[1 / 9, 1 / 9, 1 / 9],
                  [1 / 9, 1 / 9, 1 / 9],
                  [1 / 9, 1 / 9, 1 / 9]])
         
        img = fn.FilterImage(imageIn,filter0)
        
        img = ImageTk.PhotoImage(img)
        w, h = img.width(), img.height()
        
        v_canvas_output.image = img
        v_canvas_output.config(width=w, height=h)
        v_canvas_output.create_image(0, 0, image=img, anchor=tk.NW)
    except:
        print("error show image outout")
        
# ----------------------------------------------------
root = tk.Tk()
root.geometry("800x600+300+50")
root.title('iris recognition ')
# ----------------------------------------------------
v_canvas_input=tk.Canvas(root, width=300, height=200, background='white')
v_canvas_input.grid(row=1,column=0,columnspan=10)
# v_canvas.pack()
# ----------------------------------------------------
v_canvas_output=tk.Canvas(root, width=300, height=200, background='white')
v_canvas_output.grid(row=3,column=0,columnspan=10)
# v_canvas.pack()
# ----------------------------------------------------
v_bt_path1= tk.Button(root,text="select image")
v_bt_path1.grid(row=0,column=0)
v_bt_path1.config(command = lambda : getPath()  )
# ----------------------------------------------------
v_pathVar_input = tk.StringVar(root)
v_path_input = tk.Entry(root,textvariable=v_pathVar_input,width=100)
v_path_input.bind("<Return>", lambda x: Showimg(v_pathVar_input.get()))
v_path_input.grid(row=0,column=1,columnspan=8)
# ----------------------------------------------------
v_bt_Histogram= tk.Button(root,text="Histogram")
v_bt_Histogram.grid(row=2,column=0)
v_bt_Histogram.config(command = lambda : ShowHistogram()  )
# ----------------------------------------------------
v_bt_Lissage= tk.Button(root,text="Lissage")
v_bt_Lissage.grid(row=2,column=1)
v_bt_Lissage.config(command = lambda : ShowLissage()  )

root.mainloop()
