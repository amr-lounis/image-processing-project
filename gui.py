from tkinter import *
import tkinter as tk
import tkinter as ttk
from tkinter import *  
from tkinter import filedialog
from PIL import ImageTk, Image

# def getFilePath():
#     f = filedialog.askopenfilename()
#     print(f)
#     picture = Image.open(f)
#     tk_picture = ImageTk.PhotoImage(picture)
#     image_widget = tkinter.Label(window, image=tk_picture)
#     image_widget.place(x=0, y=0, width=picture_width, height=picture_height)
    
#     img = Image.open(f)
#     # imgTK =ImageTk.PhotoImage(img)
#     # v_image1(image =imgTK)

global img
def f_b1(): 
    f = filedialog.askopenfilename()
    img = ImageTk.PhotoImage(Image.open(f))   
    
root = Tk()

root.geometry("700x600")
root.title('iris recognition ')

v_label = Label(root,text= "path")
v_label.grid(row=0,column=0,padx=10,pady=10)

# v_path = ttk.Entry(root,width=10,font=("Arial",16) )
# v_path.grid(row=0,column=1,columnspan=2,pady=10)

# v_bt_path1= tk.Button(root,text="select image",command = f_b1)
# v_bt_path1.grid(row=0,column=3,pady=10)


# im = Image.open(p)
# photo = PhotoImage(im)
# # photo = photo.subsample(2)
# canvas = Canvas(root, width = 300, height = 300)

 
# canvas.create_image(20, 20, anchor=NW, image=photo) 

# canvas = Canvas(root, width = 300, height = 300)  
# canvas.grid(row=1,column=1,padx=10,pady=10)
# canvas.pack()  

p = "D:/img/12.jpg"
im= Image.open(p)
im.thumbnail((300, 300), Image.ANTIALIAS)
canvas = Canvas(root,width=300,height=300) 
canvas.grid(row=1,column=0,pady=10)
canvas.pack()  
img = ImageTk.PhotoImage(im)  
canvas.create_image(20, 20, anchor=NW, image=img) 

# # root.withdraw()



# pp = "C:/Users/pc/Desktop/befur delete/asas.PNG"
# # f = filedialog.askopenfilename()
# # print(f)
# img = Image.open(pp)
# img.thumbnail((96, 170), Image.ANTIALIAS)
# photo = ImageTk.PhotoImage(img)
# label = tk.Label(root, image=photo)
  
# v_image1 = ttk.Label(root,image= im1)
# v_image1.grid(row=1,column=1,columnspan=2,pady=10)



root.mainloop()

