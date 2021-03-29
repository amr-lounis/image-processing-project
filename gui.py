from PIL import ImageTk, Image
from tkinter import filedialog

import functions as fn
import tkinter as tk
import numpy as np
    
# ----------------------------------------------------
def CanvasInSet(_img):
    photo = ImageTk.PhotoImage(_img)
    w, h = photo.width(), photo.height()
    v_canvas_input.image = photo
    v_canvas_input.config(width=w, height=h)
    v_canvas_input.create_image(0, 0, image=photo, anchor=tk.NW)
    
# ----------------------------------------------------   
def CanvasOutSet(_img):
    photo = ImageTk.PhotoImage(_img)
    w, h = photo.width(), photo.height()
    v_canvas_output.image = photo
    v_canvas_output.config(width=w, height=h)
    v_canvas_output.create_image(0, 0, image=photo, anchor=tk.NW)
    
# ----------------------------------------------------
def getPath()-> None:
    filename = filedialog.askopenfilename()
    print("selected file : ",filename)
    v_path_input.delete(0,"end")
    v_path_input.insert(0, filename)
    print("selected file in entry ",v_pathVar_input.get())
    
    ShowImage(v_pathVar_input.get())
    
# ----------------------------------------------------   
def ShowImage(filename):
    try:
        imgArray = fn.ReadImage2d_Array(filename)
        img = fn.Convert_Array2Image(imgArray)
        CanvasInSet(img)
    except:
        print("error show image")
        
# ----------------------------------------------------
def ShowHistogram():
    try:
        filename =v_pathVar_input.get()
        imgArray = fn.ReadImage2d_Array(filename) 
        h = fn.Histogram_Array(imgArray)
        CanvasOutSet(h)
    except:
        print("error show image outout")
# ----------------------------------------------------
def ShowLissage(_filter):
    try:
        filename =v_pathVar_input.get()
        imgArray = fn.ReadImage2d_Array(filename)        
        imgArrayOut = fn.Filter_Array(imgArray,_filter)
        imgOut = fn.Convert_Array2Image(imgArrayOut)
        CanvasOutSet(imgOut)
    except:
        print("error show image outout")
# ----------------------------------------------------
root = tk.Tk()
# root.geometry("800x600+300+50")
root.title('iris recognition ')
# root.geometry('{}x{}'.format(460, 350))
# ***************************************************************************** Select Image
frame1 = tk.Frame(root)
frame1.grid(row=0,column=0)
frame1.config(width=200,height=200,relief=tk.RIDGE)
# ---------------------------------------------------- Button select image
v_bt_path1= tk.Button(frame1,text="select image")
v_bt_path1.grid(row=0,column=0)
v_bt_path1.config(command = lambda : getPath()  )
# ---------------------------------------------------- Entry path of image in
v_pathVar_input = tk.StringVar(frame1)
v_path_input = tk.Entry(frame1,textvariable=v_pathVar_input,width=100)
v_path_input.bind("<Return>", lambda x: ShowImage(v_pathVar_input.get()))
v_path_input.grid(row=0,column=1,columnspan=10)
# ***************************************************************************** Canvas
frame2 = tk.Frame(root)
frame2.grid(row=1,column=0)
frame2.config(width=200,height=200,relief=tk.RIDGE)
# ---------------------------------------------------- Canvas in
v_canvas_input=tk.Canvas(frame2, width=300, height=200, background='white')
v_canvas_input.grid(row=0,column=0)
# ---------------------------------------------------- Canvas Out
v_canvas_output=tk.Canvas(frame2, width=300, height=200, background='white')
v_canvas_output.grid(row=0,column=1)
# ***************************************************************************** Histogram
frame3 = tk.Frame(root)
frame3.grid(row=2,column=0)
frame3.config(width=200,height=200,relief=tk.RIDGE)
# ---------------------------------------------------- Button calcule and draw Histogram
v_bt_Histogram= tk.Button(frame3,text="Histogram")
v_bt_Histogram.grid(row=0,column=0)
v_bt_Histogram.config(command = lambda : ShowHistogram()  )
# # ***************************************************************************** Lissage
frame4 = tk.Frame(root)
frame4.grid(row=3,column=0)
frame4.config(width=200,height=200,relief=tk.RIDGE)
filter1 = np.array([
    [0    , 1 / 9, 0      ],
    [1 / 9, 5 / 9, 1 / 9],
    [0    , 1 / 9,0       ]
    ])
filter2 = np.array([
    [1 / 9, 1 / 9, 1 / 9],
    [1 / 9, 1 / 9, 1 / 9],
    [1 / 9, 1 / 9, 1 / 9]
    ])
filter3 = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1 ]
    ])
filter4 = np.array([
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1 ]
    ])
# ---------------------------------------------------- Button Lissage 1
v_bt_Lissage1= tk.Button(frame4,text="Lissage 5/9")
v_bt_Lissage1.grid(row=0,column=0)         
v_bt_Lissage1.config(command = lambda : ShowLissage(filter1)  )
# ---------------------------------------------------- Button Lissage 2
v_bt_Lissage2= tk.Button(frame4,text="Lissage 1/9")
v_bt_Lissage2.grid(row=0,column=1)
v_bt_Lissage2.config(command = lambda : ShowLissage(filter2)  )
# ---------------------------------------------------- Button Lissage 3
v_bt_Lissage2= tk.Button(frame4,text="contours v")
v_bt_Lissage2.grid(row=0,column=2)
v_bt_Lissage2.config(command = lambda : ShowLissage(filter3)  )
# ---------------------------------------------------- Button Lissage 4
v_bt_Lissage2= tk.Button(frame4,text="contours h")
v_bt_Lissage2.grid(row=0,column=3)
v_bt_Lissage2.config(command = lambda : ShowLissage(filter4)  )
# ----------------------------------------------------
# ***************************************************************************** Amélioration du contraste
frame5 = tk.Frame(root)
frame5.grid(row=4,column=0)
frame5.config(width=200,height=200,relief=tk.RIDGE)
# ----------------------------------------------------



root.mainloop()
