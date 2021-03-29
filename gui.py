from PIL import ImageTk, Image, ImageDraw
from tkinter import filedialog

import functions as fn
import tkinter as tk
import numpy as np

# ---------------------------------------------------- 
def creteButton(_frame,_name,_func,_v):
   return tk.Button( _frame,text=_name,width = 20,padx = 20,command = lambda : _func(_v)).pack(side=tk.LEFT)
# ----------------------------------------------------
def CanvasInSet(_img):
    _img.thumbnail((600, 400), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(_img)
    w, h = photo.width(), photo.height()
    v_canvas_input.image = photo
    v_canvas_input.config(width=w, height=h)
    v_canvas_input.create_image(0, 0, image=photo, anchor=tk.NW)
    
# ----------------------------------------------------   
def CanvasOutSet(_img):
    global ImageOutput 
    ImageOutput = _img
    _img.thumbnail((600, 400), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(_img)
    w, h = photo.width(), photo.height()
    v_canvas_output.image = photo
    v_canvas_output.config(width=w, height=h)
    v_canvas_output.create_image(0, 0, image=photo, anchor=tk.NW)
    
# ----------------------------------------------------
def getPath(_v)-> None:
    filename = filedialog.askopenfilename()
    print("selected file : ",filename)
    v_path_input.delete(0,"end")
    v_path_input.insert(0, filename)
    print("selected file in entry ",v_pathVar_input.get())
    
    ShowImage()
    
# ----------------------------------------------------   
def ShowImage():
    try:
        filename = v_pathVar_input.get()
        imgArray = fn.ReadImage2d_Array(filename)
        img = fn.Convert_Array2Image(imgArray)
        CanvasInSet(img)
    except:
        print("error show image")
        
# ----------------------------------------------------
def ShowHistogram(_v):
    try:
        filename =v_pathVar_input.get()
        imgArray = fn.ReadImage2d_Array(filename) 
        h = fn.Histogram_Array(imgArray)
        CanvasOutSet(h)
    except:
        print("error show image outout")
# ----------------------------------------------------
def ShowLissage(_v):
    print("ShowLissage:",_v)
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
    try:
        filename =v_pathVar_input.get()
        imgArray = fn.ReadImage2d_Array(filename)  
        
        if   _v == 1 :
           imgArrayOut = fn.Filter_Array(imgArray,filter1)
        elif _v == 2 :
            imgArrayOut = fn.Filter_Array(imgArray,filter2)
        elif _v == 3 :
            imgArrayOut = fn.Filter_Array(imgArray,filter3)
        elif _v == 4 :
            imgArrayOut = fn.Filter_Array(imgArray,filter4)
        else:
            print("error Filter")
        
        imgOut = fn.Convert_Array2Image(imgArrayOut)
        CanvasOutSet(imgOut)
    except:
        print("error show image outout")
        
# ----------------------------------------------------
def Segmentation(_v):
    try:
        filename =v_pathVar_input.get()
        imgArray = fn.ReadImage2d_Array(filename)   
        
        if   _v == 1 :
            iris_x,iris_y,iris_r = fn.iris(imgArray)
            pupil_x,pupil_y,pupil_r = fn.pupil(imgArray)
            
            imgArray = fn.zeroExternalArray(imgArray,iris_x,iris_y,iris_r)
            imgArray = fn.zeroInternalArray(imgArray,pupil_x, pupil_y, pupil_r)
            
            img = fn.Convert_Array2Image(imgArray)
    
            CanvasOutSet(img)
        elif _v == 2 :
            filename = filedialog.asksaveasfilename(defaultextension=".bmp",title = "Select file", filetypes=(("bmp file", "*.bmp"),("All Files", "*.*") ))
            if not filename:
                return
            
            global ImageOutput 
            print("save as :",filename)
            ImageOutput.save(filename)
        else:
            print("error Filter")
    
        # v_canvas_output.create_circle(pupil_x, pupil_y, pupil_r, outline="#00F", width=4)
        # v_canvas_output.create_circle(iris_x, iris_y, iris_r, outline="#F00", width=4)
    except:
        print("error show image outout")
# ----------------------------------------------------  
def Morphologiques(_v):
    try:
        filename = v_pathVar_input.get()
        imgArray = fn.ReadImage2d_Array(filename) 
        thresholding = scale1.get() 
        imgBiColor255 = np.where(imgArray > thresholding, 255, 0)
        
        kernel = np.array ([
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0]
            ], dtype = np.uint8)

        if _v == 1:
            imgOut = fn.Convert_Array2Image(imgBiColor255)
            CanvasOutSet(imgOut)
        if _v == 2:
            imgBiner = np.where(imgBiColor255 == 255, 1, 0)
            imgoutErosion = fn.Erosion_Array(imgBiner,kernel)
            imgoutErosion255 = np.where(imgoutErosion == 1, 255, 0)
            imgOut = fn.Convert_Array2Image(imgoutErosion255)
            CanvasOutSet(imgOut)
        elif _v==3:
            imgBiner = np.where(imgBiColor255 == 255, 1, 0)
            imgoutErosion = fn.Dilation_Array(imgBiner,kernel)
            imgoutErosion255 = np.where(imgoutErosion == 1, 255, 0)
            imgOut = fn.Convert_Array2Image(imgoutErosion255)
            CanvasOutSet(imgOut)

    except:
        print("error show image outout")
# ---------------------------------------------------- 
         
"""  ***************************************************************************** ROOT """ 
root = tk.Tk()
root.geometry("800x600+300+50")
root.title('iris recognition ')
ImageOutput = None
v = tk.IntVar()
v.set(1)
"""  ***************************************************************************** Frame Select Image """ 
frame1 = tk.Frame(root)
frame1.pack()
# ---------------------------------------------------- Button select image
creteButton(frame1,"Select",getPath,1)
# # ---------------------------------------------------- Entry path of image in
v_pathVar_input = tk.StringVar(frame1)
v_path_input = tk.Entry(frame1,textvariable=v_pathVar_input,width=50)
v_path_input.bind("<Return>", lambda x: ShowImage())
v_path_input.pack(side=tk.LEFT)

"""  ***************************************************************************** Frame Canvas """ 
frame2 = tk.Frame(root)
frame2.pack()
# ---------------------------------------------------- Canvas in
v_canvas_input=tk.Canvas(frame2, width=300, height=200, background='white')
v_canvas_input.grid(row=0,column=0)
# ---------------------------------------------------- Canvas Out
v_canvas_output=tk.Canvas(frame2, width=300, height=200, background='white')
v_canvas_output.grid(row=0,column=1)

"""  ***************************************************************************** Frame Histogram """ 
frame3 = tk.Frame(root)
frame3.pack()
creteButton(frame3,"Histogram",ShowHistogram,1)
"""  ***************************************************************************** Frame Lissage """ 
frame4 = tk.Frame(root)
frame4.pack()
creteButton(frame4,"Lissage 5/9",ShowLissage,1)
creteButton(frame4,"Lissage 1/9",ShowLissage,2)
creteButton(frame4,"contours v",ShowLissage,3)
creteButton(frame4,"contours h",ShowLissage,4)
"""  ***************************************************************************** Frame Amélioration du contraste """ 
frame5 = tk.Frame(root)
frame5.pack()
"""  ***************************************************************************** Frame Segmentation par clustering """ 
frame6 = tk.Frame(root)
frame6.pack()
creteButton(frame6,"Segmentation",Segmentation,1)
creteButton(frame6,"Save",Segmentation,2)
"""  *****************************************************************************  Frame Opérations morphologiques """ 
frame7 = tk.Frame(root)
frame7.pack()
creteButton(frame7,"Seuillage",Morphologiques,1)
creteButton(frame7,"Erosion",Morphologiques,2)
creteButton(frame7,"Dilation",Morphologiques,3)

scale1 = tk.Scale(frame7,from_=0,to=255,orient=tk.HORIZONTAL,length=255)
scale1.set(50)
scale1.pack()

"""  ***************************************************************************** Frame SIFT """ 
frame8 = tk.Frame(root)
frame8.pack()
# ----------------------------------------------------


root.mainloop()