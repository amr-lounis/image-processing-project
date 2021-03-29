import numpy as np
# ****************************************************************************
def FilesYield(_dir_path,_extension):
    import os
    for root, dirs, files in os.walk(os.path.abspath(_dir_path)): 
        for file in files:
            file = str(file)
            if file.endswith(_extension):
                yield os.path.join(root, file)     
def Files(_dir_path,_extension):
    return [f for f in FilesYield(_dir_path,_extension)]

# ----------------------------------------------------------------------
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
    return imgArray
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
    return _b* imgArray + _a

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
    ax.set_ylabel("nomber repitition")   
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
def Convert_BiColor_Array(imgArray,_seullage):
    return np.where(imgArray > _seullage, 1, 0)
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
# ---------------------------------------------------------------------- Segmentation
def pupil(_ArrayBiC,valeuFind = 1):
    n_columns =_ArrayBiC.shape[1]
    n_rows =_ArrayBiC.shape[0]
    
    sumX = 0
    sumY = 0
    sumN = 0
    for y in range(0,n_rows):
        for x in range(0,n_columns):
            if _ArrayBiC[y][x] == valeuFind:
                sumX = sumX + x
                sumY = sumY + y
                sumN = sumN + 1
    
    pupilX = int(sumX/sumN)
    pupilY = int(sumY/sumN)
    pupilR = int(np.sqrt(sumN/np.pi) ) #Area of a disk =  πr^2
    return pupilX,pupilY,pupilR
# ---------------------------------------------------------------------- Segmentation
def iris(_ArrayBiC,valeuFind = 1):
    x,y,r =pupil(_ArrayBiC,valeuFind)
    return x,y,r*3

# ********************************************************************** Need opencv
# ---------------------------------------------------------------------- Détecteur SIFT
import cv2 as cv2
def Get_Keypoints_Des_Array(_imgArray):
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp, des = sift.detectAndCompute(_imgArray,None)
    # # draw keypoint
    # imgOut = cv2.drawKeypoints(img,kp,None,color=(0,255,0), flags=0)
    return kp,des,_imgArray

# ----------------------------------------------------------------------Descripteur SIFT
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

# ----------------------------------------------------------------------Distance euclidienne
def GetMatchingImageValue_Array(_imgArray1,_imgArray2):
    kp1, des1 , img1 = Get_Keypoints_Des_Array(_imgArray1)
    kp2, des2 , img2 = Get_Keypoints_Des_Array(_imgArray2)
    good = GetMatching(des1,des2)

    # print ("matches found : %d" % (len(good)))
    imgOut = cv2.drawMatches(img1,kp1,img2,kp2,good,None ,**dict(matchColor = (0,255,0),flags = 0))
    return imgOut , len(good)
# ****************************************************************************