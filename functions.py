import numpy as np
from PIL import Image

# ****************************************************************************
import os
def FilesYield(_dir_path,_extension):
    for root, dirs, files in os.walk(os.path.abspath(_dir_path)): 
        for file in files:
            file = str(file)
            if file.endswith(_extension):
                yield os.path.join(root, file)     
def Files(_dir_path,_extension):
    return [f for f in FilesYield(_dir_path,_extension)]

def Hexencode(rgb):
    r=rgb[0]
    g=rgb[1]
    b=rgb[2]
    return '#%02x%02x%02x' % (r,g,b)

def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img
# ****************************************************************************

import cv2 as cv2
def GetKeypointsDesImg(_img):
    # read image
    # img = cv2.imread(p_path, 0)
    img = np.array(_img) 
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp, des = sift.detectAndCompute(img,None)
    # # draw keypoint
    # imgOut = cv2.drawKeypoints(img,kp,None,color=(0,255,0), flags=0)
    # cv2.imshow('keypoint', imgOut)
    # plt.imshow(imgOut, 'gray'),plt.show()
    return kp,des,img

def GetMatching(des1,des2):
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # store all the good matches as per Lowe's ratio test.
    goodMatchs = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            goodMatchs.append(m)
    return goodMatchs

def GetMatchingImageValue(_img1,_img2):
    kp1, des1 , img1 = GetKeypointsDesImg(_img1)
    kp2, des2 , img2 = GetKeypointsDesImg(_img2)
    good = GetMatching(des1,des2)

    # print ("matches found : %d" % (len(good)))
    imgOut = cv2.drawMatches(img1,kp1,img2,kp2,good,None ,**dict(matchColor = (0,255,0),flags = 0))
    return imgOut , len(good)

# ****************************************************************************
def ContrastLinear(_img,_b,_a):
    imgArray = np.array(_img)
    
    x=_b* imgArray + _a
    
    imgout=Image.fromarray(x.astype(np.uint8))
    return imgout

def ContrastInvers(_img):
    imgArray = np.array(_img)
    
    x=255- imgArray
    
    imgout=Image.fromarray(x.astype(np.uint8))
    return imgout

def ContrastLog(_img):
    imgArray = np.array(_img)
    
    x = np.abs(np.log(imgArray+1.1)*255 /
               np.log(np.max(imgArray+1.1)))
    
    imgout=Image.fromarray(x.astype(np.uint8))
    return imgout

def ContrastRange(_img,_min,_max):
    imgArray = np.array(_img)
    # print("max",np.max(imgArray),"min",np.min(imgArray))   
    for i in range(0,imgArray.shape[0]):
        for j in range(0,imgArray.shape[1]):
            imgArray[i][j]= int(255/(_max-_min) * (imgArray[i][j] - _min ))
            if imgArray[i][j] > 255:
                imgArray[i][j] = 255
            elif imgArray[i][j] <0:
                imgArray[i][j] = 0
    print("max",np.max(imgArray),"min",np.min(imgArray))        
    imgout=Image.fromarray(imgArray.astype(np.uint8))     
    return imgout
# ****************************************************************************

def ConvertImage_2d(_img):
    imgArray = np.array(_img)
        
    if len(imgArray.shape) == 2:
        n_line = imgArray.shape[0]
        n_cols = imgArray.shape[1]
        print("matrix 2 D","row",n_line,"col",n_cols)
    else:
        n_line = imgArray.shape[0]
        n_cols = imgArray.shape[1]
        n_3 = imgArray.shape[2]
        print("matrix 3 D","row",n_line,"col",n_cols,"d_3",n_3)
        matrix2D = np.zeros((n_line,n_cols), np.uint64)
        for i in range(0,n_line):
            for j in range(0,n_cols):
                val= int((imgArray[i,j,0]+imgArray[i,j,1]+imgArray[i,j,2])/3)
                matrix2D[i,j]= val
                
    imgout=Image.fromarray(imgArray.astype(np.uint8))     
    return imgout

def ConvertImage_BiColor(_img,_seullage):
    imgArray = np.array(_img)
    
    mt_bi = np.where(imgArray > _seullage, 1, 0)
    
    return Image.fromarray(mt_bi.astype(np.uint8))

def Histogram_Image(_img):
    from matplotlib.figure import Figure

    imgArray = np.array(_img)
    
    y = np.zeros(256, np.uint32)
    for i in range(0,imgArray.shape[0]):
        for j in range(0,imgArray.shape[1]):
            y[imgArray[i,j]] += 1
    
    fig = Figure()
    ax = fig.subplots()
    ax.set_xlabel("value of pixel")
    ax.set_ylabel("nomber repitition")   
    ax.set_title('histogram')
    ax.plot(range(0,256),y,'black');

    img = fig2img(fig)
    # img.show()
    return img;

def FilterImage(_image,_filter3x3):
    arrayIn= np.array(_image)
    arrayOut = np.zeros(arrayIn.shape,np.uint8)
    
    for ligne in range(1,arrayIn.shape[0]-1):
        for col in range(1,arrayIn.shape[1]-1):
            # On calcule la somme 
            somme = 0
            for l in range(3):
                for c in range(3):
                    somme += _filter3x3[l,c]*arrayIn[ligne-1+l,col-1+c]
            arrayOut[ligne,col] = somme

    return Image.fromarray(arrayOut.astype(np.uint8))
# ----------------------------------------------------------------------
def add_padding(image, padding, value):
    return cv2.copyMakeBorder(image, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=value)
# ----------------------------------------------------------------------
def ErosionArray(image, kernel):
    img_operated = image.copy() #this will be the image
    padded = add_padding(image, 1, 1)  # <<< MODIFIED
    vertical_window = padded.shape[0] - kernel.shape[0] #final vertical window position
    horizontal_window = padded.shape[1] - kernel.shape[1] #final horizontal window position
    vertical_pos = 0
    while vertical_pos <= vertical_window:
        horizontal_pos = 0
        while horizontal_pos <= horizontal_window:
            erosion_flag = False
            for i in range(kernel.shape[0]):      # <<< MODIFIED
                for j in range(kernel.shape[1]):  # <<< MODIFIED
                    if kernel[i][j] == 1:         # <<< ADDED
                        #First Case
                        if True:
                            #if we find 0, then break the second loop
                            if padded[vertical_pos+i][horizontal_pos+j] == 0:  # <<< MODIFIED
                                erosion_flag = True                            # <<< MODIFIED
                                break
                if erosion_flag:         # <<< MODIFIED
                    img_operated[vertical_pos, horizontal_pos] = 0  # <<< ADDED
                    break

            horizontal_pos += 1
        vertical_pos += 1
    return img_operated
# ----------------------------------------------------------------------
def DilationArray(image, kernel):
    img_operated = image.copy() #this will be the image  # <<< ADDED
    padded = add_padding(image, 1, 0)  # <<< MODIFIED
    vertical_window = padded.shape[0] - kernel.shape[0] #final vertical window position
    horizontal_window = padded.shape[1] - kernel.shape[1] #final horizontal window position
    vertical_pos = 0
    while vertical_pos <= vertical_window:
        horizontal_pos = 0
        while horizontal_pos <= horizontal_window:
            dilation_flag = False
            erosion_flag = False
            for i in range(kernel.shape[0]):      # <<< MODIFIED
                for j in range(kernel.shape[1]):  # <<< MODIFIED
                    if kernel[i][j] == 1:  
                        if padded[vertical_pos+i][horizontal_pos+j] == 1:  # <<< MODIFIED
                            dilation_flag = True
                            break
                if dilation_flag:       # <<< FIXED
                    img_operated[vertical_pos, horizontal_pos] = 1
                    break
            horizontal_pos += 1
        vertical_pos += 1
    return img_operated
# ----------------------------------------------------------------------
def ErosionImage(_image, kernel):
    imgArray = np.array(_image)
    imgArrayE = ErosionArray(imgArray,kernel)
    return Image.fromarray(imgArrayE.astype(np.uint8))
# ----------------------------------------------------------------------
def DilationImage(_image, kernel):
    imgArray = np.array(_image)
    imgArrayD = DilationArray(imgArray,kernel)
    return Image.fromarray(imgArrayD.astype(np.uint8))
# ----------------------------------------------------------------------
# array = np.array([[0,0,1,1,1,1],
#                [0,0,1,1,1,1],
#                [1,1,1,1,1,1],
#                [1,1,1,1,1,1],
#                [1,1,1,1,0,0],
#                [1,1,1,1,0,0]], dtype=np.uint8)

# kernel = np.array ([[0, 1, 0],
#                     [1, 1, 1],
#                     [0, 1, 0]], dtype = np.uint8)


# print(array)

# #image will be padded with one zeros around
# result_erosion = ErosionArray(array, kernel)
# result_dilation = DilationArray(array, kernel)
# print('result_erosion',result_erosion)
# print('result_dilation',result_dilation)