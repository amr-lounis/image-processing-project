import numpy as np
# ****************************************************************************
def Convert_fig_img(fig):
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

# ----------------------------------------------------------------------
def Convert_3d_2d_Array(imgArray):
    if len(imgArray.shape) == 2:
        # print("------------------------------------------------- Array 2d")
        n_line = imgArray.shape[0]
        n_cols = imgArray.shape[1]
        return imgArray
    
    elif len(imgArray.shape) == 3:
        # print("------------------------------------------------- Array 3d")
        n_line = imgArray.shape[0]
        n_cols = imgArray.shape[1]
        matrix2D = np.zeros((n_line,n_cols), np.uint64)
        for i in range(0,n_line):
            for j in range(0,n_cols):
                val= int((imgArray[i,j,0]+imgArray[i,j,1]+imgArray[i,j,2])/3)
                matrix2D[i,j]= val   
        return matrix2D
    else:
        print("len(imgArray.shape):",len(imgArray.shape))
        
# ----------------------------------------------------------------------
def ReadImage2d_Array(_path):
    image = Image.open(_path)
    imgArray = np.array(image)  
    return Convert_3d_2d_Array(imgArray)
# ----------------------------------------------------------------------
from PIL import Image
def Convert_Array2Image(_imgArray):
    return Image.fromarray(_imgArray.astype(np.uint8))
# ---------------------------------------------------------------------- Contrast
def ContrastLinear_Array(imgArray,_b,_a):
    imgArray =  imgArray.copy()
    for i in range(0,imgArray.shape[0]):
        for j in range(0,imgArray.shape[1]):
            imgArray[i][j]= int(imgArray[i][j]*_b+_a)
            if imgArray[i][j] > 255:
                imgArray[i][j] = 255
            elif imgArray[i][j] <0:
                imgArray[i][j] = 0
    return imgArray

# ---------------------------------------------------------------------- Contrast
def ContrastInvers_255_Array(imgArray):
    return 255- imgArray

# ---------------------------------------------------------------------- Contrast
def ContrastInvers_BiC_Array(imgArray):
    return 1- imgArray

# ---------------------------------------------------------------------- Contrast
def ContrastLog_Array(imgArray):
    return np.abs(np.log(imgArray+1.1)*255 /
               np.log(np.max(imgArray+1.1)))

# ---------------------------------------------------------------------- Contrast
def ContrastRange_Array(imgArray,_min,_max): 
    imgArray =  imgArray.copy()
    for i in range(0,imgArray.shape[0]):
        for j in range(0,imgArray.shape[1]):
            imgArray[i][j]= int(255/(_max-_min) * (imgArray[i][j] - _min ))
            if imgArray[i][j] > 255:
                imgArray[i][j] = 255
            elif imgArray[i][j] <0:
                imgArray[i][j] = 0
    return imgArray

# ----------------------------------------------------------------------  Egalisation d’histogramme
def Histogram_Array(imgArray):
    from matplotlib.figure import Figure
    y = np.zeros(256, np.uint32)
    for i in range(0,imgArray.shape[0]):
        for j in range(0,imgArray.shape[1]):
            y[imgArray[i,j]] += 1
    
    fig = Figure()
    ax = fig.subplots()
    ax.set_xlabel("value of pixel")
    ax.set_ylabel("pixel frequency")   
    ax.set_title('histogram')
    ax.plot(range(0,256),y,'black');

    img = Convert_fig_img(fig)
    return img;

# ---------------------------------------------------------------------- Lissage des images
def Filter_Array(_arrayIn,_filter3x3):
    arrayOut = np.zeros(_arrayIn.shape,np.uint8) 
    for ligne in range(1,_arrayIn.shape[0]-1):
        for col in range(1,_arrayIn.shape[1]-1):
            # On calcule la somme 
            somme = 0
            for l in range(3):
                for c in range(3):
                    somme += _filter3x3[l,c]*_arrayIn[ligne-1+l,col-1+c]
            arrayOut[ligne,col] = somme
    return arrayOut

# ---------------------------------------------------------------------- Opérations morphologiques
def Convert_BiColor_Array(imgArray,_thresholding):
    return np.where(imgArray > _thresholding, 1, 0)
# ---------------------------------------------------------------------- Opérations morphologiques
def Erosion_Array(image, kernel):
    img_operated = image.copy() #this will be the image
    vertical_window = image.shape[0] - kernel.shape[0] #final vertical window position
    horizontal_window = image.shape[1] - kernel.shape[1] #final horizontal window position
    vertical_pos = 0
    while vertical_pos <= vertical_window:
        horizontal_pos = 0
        while horizontal_pos <= horizontal_window:
            erosion_flag = False
            for i in range(kernel.shape[0]):      # <<< MODIFIED
                for j in range(kernel.shape[1]):  # <<< MODIFIED
                    if kernel[i][j] == 1:         # <<< ADDED
                        if image[vertical_pos+i][horizontal_pos+j] == 0:  # <<< MODIFIED
                            erosion_flag = True                            # <<< MODIFIED
                            break
                if erosion_flag:         # <<< MODIFIED
                    img_operated[vertical_pos, horizontal_pos] = 0  # <<< ADDED
                    break

            horizontal_pos += 1
        vertical_pos += 1
    return img_operated

# ---------------------------------------------------------------------- Opérations morphologiques
def Dilation_Array(image, kernel):
    img_operated = image.copy() #this will be the image  # <<< ADDED
    vertical_window = image.shape[0] - kernel.shape[0] #final vertical window position
    horizontal_window = image.shape[1] - kernel.shape[1] #final horizontal window position
    vertical_pos = 0
    while vertical_pos <= vertical_window:
        horizontal_pos = 0
        while horizontal_pos <= horizontal_window:
            dilation_flag = False
            for i in range(kernel.shape[0]):      # <<< MODIFIED
                for j in range(kernel.shape[1]):  # <<< MODIFIED
                    if kernel[i][j] == 1:  
                        if image[vertical_pos+i][horizontal_pos+j] == 1:  # <<< MODIFIED
                            dilation_flag = True
                            break
                if dilation_flag:       # <<< FIXED
                    img_operated[vertical_pos, horizontal_pos] = 1
                    break
            horizontal_pos += 1
        vertical_pos += 1
    return img_operated
# ---------------------------------------------------------------------- Segmentation pupil
def pupil(_imgArray,_seullage, valeuFind):
    n_columns =_imgArray.shape[1]
    n_rows =_imgArray.shape[0]
    
    imgBiC = np.where(_imgArray > _seullage, 1, 0)
        
    sumX = 0
    sumY = 0
    sumN = 0
    for y in range(0,n_rows):
        for x in range(0,n_columns):
            if imgBiC[y][x] == valeuFind:
                sumX = sumX + x
                sumY = sumY + y
                sumN = sumN + 1
    
    X = int(sumX/sumN)
    Y = int(sumY/sumN)
    R = int(np.sqrt(sumN/np.pi) ) #Area of a disk =  πr^2
    return X,Y,R
# ---------------------------------------------------------------------- Segmentation iris
def iris(_imgArray,_seullage, valeuFind):
    x,y,r =pupil(_imgArray,_seullage,valeuFind)
    return x,y,r*2
# ---------------------------------------------------------------------- Segmentation color white in external cyrle 
def WipeOutCircle(_array,_x,_y,_r):
    _array = _array.copy()
    for i in range(0,_array.shape[0]):
        for j in range(0,_array.shape[1]):
            if( (j-_x)**2 + (i-_y)**2 ) >= _r**2:
                _array[i][j]=255
    return _array
# ---------------------------------------------------------------------- Segmentation color black in internal cyrle           
def WipeInsideCircle(_array,_x,_y,_r):
    _array = _array.copy()    
    for i in range(0,_array.shape[0]):
        for j in range(0,_array.shape[1]):
            if( (j-_x)**2 + (i-_y)**2 ) <= _r**2:
                _array[i][j]=0
    return _array
# ---------------------------------------------------------------------- All Segmentation 
def Segmentation(_imgArray,_seullage = 50, valeuFind = 0):
    pupil_x,pupil_y,pupil_r = pupil(_imgArray,_seullage,valeuFind)
    iris_x,iris_y,iris_r = iris(_imgArray,_seullage,valeuFind)
    
    _imgArray = WipeOutCircle(_imgArray,iris_x,iris_y,iris_r)
    _imgArray = WipeInsideCircle(_imgArray,pupil_x, pupil_y, pupil_r)
 
    return _imgArray,(pupil_x,pupil_y,pupil_r),(iris_x,iris_y,iris_r)
 
# ********************************************************************** Need opencv
# ---------------------------------------------------------------------- Détecteur SIFT
import cv2 as cv2
import os
# ---------------------------------------------------------------------- Descripteur Distance  SIFT
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

# ---------------------------------------------------------------------- Create database of valeu des and path file
_listSIFT = []
def AddIrisToDatabase(_list):
    global _listSIFT
    sift = cv2.xfeatures2d.SIFT_create()
    for f in _list:
        try:
            imgArray = ReadImage2d_Array(f)
            # imgArray ,pupil,iris = Segmentation(imgArray)   # ------------ Segmentation all iris 
            kp, des = sift.detectAndCompute(imgArray,None)  # ------------ Descriptor of iris after Segmentation
            _listSIFT.append([f,des])
        except:
            print("Error read file:",f)

# ---------------------------------------------------------------------- 
def Recognition(_path):
    try:
        sift = cv2.xfeatures2d.SIFT_create()
        global _listSIFT
        imgArray1 = ReadImage2d_Array(_path) 
        # imgArray1 ,pupil,iris = Segmentation(imgArray1)   # ------------ Segmentation iris ( l'échantillon )
        kp1, des1 = sift.detectAndCompute(imgArray1,None) # ------------ Descriptor of iris after Segmentation
        
        maxMatching =0
        maxGood = []
        maxPos = 0
        index = 0
       
        for v in _listSIFT:
            good = GetMatching(des1,v[1])
            if len(good) >= maxMatching:
                maxPos = index
                maxMatching = len(good)
                maxGood = good
            index = index+1      
        
        print("SIFT Matching max value is:",maxMatching,"path:",_listSIFT[maxPos][0])
        
        # ------------------------------------------------------ this for chowing matching 
        path2 = _listSIFT[maxPos][0]  #-------------- This is the path of the recognized image
        imgArray2 = ReadImage2d_Array(path2) #-------------- read image from database
        # imgArray2 ,pupil2,iris2 = Segmentation(imgArray2)    # ------------ Segmentation iris That have been recognized
        kp2, des2 = sift.detectAndCompute(imgArray2,None)    # ------------ Descriptor and keypoint of iris after Segmentation
        imgArrayOut = cv2.drawMatches(imgArray1,kp1,imgArray2,kp2,maxGood,None ,**dict(matchColor = (0,255,0),flags = 2)) # drawing
        
        imgOut = Convert_Array2Image(imgArrayOut)
        return imgOut,maxMatching,os.path.basename(path2)
        
    except:
        print("Error Recon:")

# ****************************************************************************