from PIL import ImageTk ,Image
from tkinter import filedialog

import functions as fn
import tkinter as tk
import numpy as np

from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror

# ---------------------------------------------------- 
def creteButton(_frame,_name,_func,_v):
   return tk.Button( _frame,text=_name,width = 20,padx = 20,command = lambda : _func(_v)).pack(side=tk.LEFT)
# ----------------------------------------------------

def Mbox(title, text, style):
    showinfo(title=title, message=text)
    
def errorOutput():
    showerror(title="Error", message="error : There is a problem showing the results \n Please select the picture")
"""  ***************************************************************************** ROOT """ 
root = tk.Tk()
root.geometry("1000x600+300+50")
root.title('iris recognition ')
# ----------------------------------------------------
ImageOutput = None
# ----------------------------------------------------
v = tk.IntVar()
v.set(1)
# ----------------------------------------------------
listFram =[]
for i in range(0,10):
    listFram.append(tk.Frame(root))
    listFram[i].pack()
frameN=-1
"""  ***************************************************************************** Frame Select Image """ 
frameN= frameN+1
# ----------------------------------------------------
def getPath(_v)-> None:
    filename = filedialog.askopenfilename(initialdir='./',defaultextension=".bmp",title = "Select file", filetypes=(("bmp file", "*.bmp"),("All Files", "*.*") ))
    if filename == None :
        return
    v_path_input.delete(0,"end")
    v_path_input.insert(0, filename)
    ShowImage()
    
# ----------------------------------------------------   
def ShowImage():
    try:
        filename = v_pathVar_input.get()
        imgArray = fn.ReadImage2d_Array(filename)
        img = fn.Convert_Array2Image(imgArray)
        CanvasInSet(img)
    except:
        errorOutput()
        
# ---------------------------------------------------- Button select image
creteButton(listFram[frameN],"Select",getPath,1)
# # ---------------------------------------------------- Entry path of image in
v_pathVar_input = tk.StringVar(listFram[frameN])
v_path_input = tk.Entry(listFram[frameN],textvariable=v_pathVar_input,width=50)
v_path_input.bind("<Return>", lambda x: ShowImage())
v_path_input.pack(side=tk.LEFT)

"""  ***************************************************************************** Frame Canvas """ 
frameN=frameN+1
# ---------------------------------------------------- 
def CanvasInSet(_img):
    try:
        _img.thumbnail((600, 400), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(_img)
        w, h = photo.width(), photo.height()
        v_canvas_input.image = photo
        v_canvas_input.config(width=w, height=h)
        v_canvas_input.create_image(0, 0, image=photo, anchor=tk.NW)
    except:
        errorOutput()

    
# ----------------------------------------------------   
def CanvasOutSet(_img):
    global ImageOutput 
    try:
        ImageOutput = _img
        _img.thumbnail((600, 400), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(_img)
        w, h = photo.width(), photo.height()
        v_canvas_output.image = photo
        v_canvas_output.config(width=w, height=h)
        v_canvas_output.create_image(0, 0, image=photo, anchor=tk.NW)
    except:
       errorOutput() 

    
# ---------------------------------------------------- Canvas in
v_canvas_input=tk.Canvas(listFram[frameN], width=300, height=200, background='white')
v_canvas_input.grid(row=0,column=0)
# ---------------------------------------------------- Canvas Out
v_canvas_output=tk.Canvas(listFram[frameN], width=300, height=200, background='white')
v_canvas_output.grid(row=0,column=1)

"""  ***************************************************************************** Frame Histogram """ 
frameN=frameN+1
# ---------------------------------------------------- 
def ShowHistogram(_v):
    try:
        filename =v_pathVar_input.get()
        imgArray = fn.ReadImage2d_Array(filename) 
        imgOut = fn.Histogram_Array(imgArray)  
        CanvasOutSet(imgOut)
    except:
        errorOutput()
# ----------------------------------------------------
creteButton(listFram[frameN],"Histogram",ShowHistogram,1)

"""  ***************************************************************************** Frame Lissage """ 
frameN=frameN+1
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
        
        if   _v == 1 :                                    # using fiter1 Smoothing
           imgArrayOut = fn.Filter_Array(imgArray,filter1)
        elif _v == 2 :                                    # using fiter2 Smoothing medium filter
            imgArrayOut = fn.Filter_Array(imgArray,filter2)
        elif _v == 3 :                                    # using fiter3 vertical outlines
            imgArrayOut = fn.Filter_Array(imgArray,filter3)
        elif _v == 4 :                                    # using fiter4 horizontal outlines
            imgArrayOut = fn.Filter_Array(imgArray,filter4)
        else:
            print("error Filter")
        
        imgOut = fn.Convert_Array2Image(imgArrayOut)
        CanvasOutSet(imgOut)
    except:
        errorOutput()
# ----------------------------------------------------
creteButton(listFram[frameN],"Smoothing ",ShowLissage,1)
creteButton(listFram[frameN],"Smoothing medium filter",ShowLissage,2)
creteButton(listFram[frameN],"vertical outlines",ShowLissage,3)
creteButton(listFram[frameN],"horizontal outlines",ShowLissage,4)

"""  ***************************************************************************** Frame Amélioration du contraste """ 
frameN=frameN+1
# ---------------------------------------------------- 
def Contraste(_v):
    try:
        filename = v_pathVar_input.get()
        imgArray = fn.ReadImage2d_Array(filename) 
        
        if _v == 1:                                        #   Contrast lmin lmax
            _min,_max = 50,200
            imgOutArray = fn.ContrastRange_Array(imgArray,_min,_max)
        elif _v == 2:                                       #  Contrast Log
            imgOutArray = fn.ContrastLog_Array(imgArray)
        elif _v == 3:                                       #  Contrast Linear
            imgOutArray = fn.ContrastLinear_Array(imgArray,1.2,0)
            print(imgArray.shape)
        elif _v == 4:                                       #  Contrast Invers
            imgOutArray = fn.ContrastInvers_255_Array(imgArray)

        imgOut = fn.Convert_Array2Image(imgOutArray)
        CanvasOutSet(imgOut)
    except:
        errorOutput()
        
# ----------------------------------------------------       
creteButton(listFram[frameN],"Contrast lmin:50 lmax:200",Contraste,1)
creteButton(listFram[frameN],"Contrast Log",Contraste,2)
creteButton(listFram[frameN],"Contrast Linear",Contraste,3)
creteButton(listFram[frameN],"Contrast Invers",Contraste,4)

"""  ***************************************************************************** Frame Segmentation par clustering """ 
frameN=frameN+1
# ----------------------------------------------------
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle
# ----------------------------------------------------
def Segmentation(_v):
    try:
        if _v == 1:
            filename =v_pathVar_input.get()
            imgArray = fn.ReadImage2d_Array(filename)   
            
            imgArray ,pupil,iris = fn.Segmentation(imgArray)
            iris_x,iris_y,iris_r = iris
            pupil_x,pupil_y,pupil_r = pupil
    
            img = fn.Convert_Array2Image(imgArray)
    
            CanvasOutSet(img)
            
            v_canvas_output.create_circle(pupil_x, pupil_y, pupil_r, outline="#00F", width=4)
            v_canvas_output.create_circle(iris_x, iris_y, iris_r, outline="#F00", width=4)
            
    except:
        errorOutput()
        
creteButton(listFram[frameN],"Segmentation",Segmentation,1)

"""  *****************************************************************************  Frame Opérations morphologiques """ 
frameN=frameN+1
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

        if _v == 1:                         # Thresholding  show
            imgOut = fn.Convert_Array2Image(imgBiColor255)
            CanvasOutSet(imgOut)
        elif _v == 2:                       # Erosion
            imgBiner = np.where(imgBiColor255 == 255, 1, 0)
            imgoutErosion = fn.Erosion_Array(imgBiner,kernel)
            imgoutErosion255 = np.where(imgoutErosion == 1, 255, 0)
            imgOut = fn.Convert_Array2Image(imgoutErosion255)
            CanvasOutSet(imgOut)
        elif _v==3:                         # Dilation
            imgBiner = np.where(imgBiColor255 == 255, 1, 0)
            imgoutErosion = fn.Dilation_Array(imgBiner,kernel)
            imgoutErosion255 = np.where(imgoutErosion == 1, 255, 0)
            imgOut = fn.Convert_Array2Image(imgoutErosion255)
            CanvasOutSet(imgOut)

    except:
        errorOutput()
        
# ----------------------------------------------------       
creteButton(listFram[frameN],"Thresholding",Morphologiques,1)
scale1 = tk.Scale(listFram[frameN],from_=0,to=255,orient=tk.HORIZONTAL,length=255)
scale1.set(50)
scale1.pack(side=tk.LEFT)

creteButton(listFram[frameN],"Erosion",Morphologiques,2)
creteButton(listFram[frameN],"Dilation",Morphologiques,3)

"""  ***************************************************************************** Save """ 
frameN=frameN+1
# ----------------------------------------------------
def SaveOutput(_v):
    try:
        filename = filedialog.asksaveasfilename(initialdir='./',defaultextension=".bmp",title = "Select file", filetypes=(("bmp file", "*.bmp"),("All Files", "*.*") ))
        if not filename:
            return
        
        global ImageOutput 
        print("save as :",filename)
        ImageOutput.save(filename)
        Mbox("Save","Image is saved to: ( {} )".format(filename),0)
    except:
        errorOutput()
# ----------------------------------------------------        
creteButton(listFram[frameN],"Save",SaveOutput,1)
"""  ***************************************************************************** Frame SIFT """
frameN=frameN+1
# ----------------------------------------------------
def AddIrisToDatabase (_v):
    files = filedialog.askopenfilenames(initialdir='./',defaultextension=".bmp",title = "Select file", filetypes=(("bmp file", "*.bmp"),("All Files", "*.*") ))
    fn.AddIrisToDatabase(files)
    Mbox("Database SIFT","The number of iris available is :( {} )".format(len(fn._listSIFT)),0)
creteButton(listFram[frameN],"Add iris to Database",AddIrisToDatabase,1)
# ----------------------------------------------------
def checkDatabase (_v):
    Mbox("database","The number of iris available is :( {} )".format(len(fn._listSIFT)),0)
creteButton(listFram[frameN],"check Database ",checkDatabase,1)
# ----------------------------------------------------
def Recognition (_v):
    file = filedialog.askopenfilename(initialdir='./',defaultextension=".bmp",title = "Select file", filetypes=(("bmp file", "*.bmp"),("All Files", "*.*") ))
    try:
        imgOut , v , p= fn.Recognition(file)
        CanvasOutSet(imgOut)
        if v >= 10: 
            varl.set("SIFT Matching max value is:( {} )\n Recognition :( {} )".format(v,p) )
        else:
            varl.set("SIFT Matching max value is:( {} )\n This iris is not recognized in database \n But it is similar ( {} )".format(v,p) )
    except:
        varl.set("Database SIFT Size =: ( 0 )" )

creteButton(listFram[frameN],"Recognition ",Recognition,1)
varl = tk.StringVar()
varl.set("----------------------" )
l = tk.Label(listFram[frameN],textvariable = varl,bg='#fff',fg='#000',font=15)
l.pack(side=tk.LEFT)
# ----------------------------------------------------
root.mainloop()