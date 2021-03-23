import numpy as np
from PIL import Image
# ****************************************************************************
import cv2 as cv2
def getKeypointsDesImg(_img):
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

def getMatching(des1,des2):
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

def getMatchingNumber(_img1,_img2):
    kp1, des1 , img1 = getKeypointsDesImg(_img1)
    kp2, des2 , img2 = getKeypointsDesImg(_img2)
    good = getMatching(des1,des2)

    # print ("matches found : %d" % (len(good)))
    imgOut = cv2.drawMatches(img1,kp1,img2,kp2,good,None ,**dict(matchColor = (0,255,0),flags = 0))
    return imgOut , len(good)

# ****************************************************************************
def ImgLinear(_imgArray,_b,_a):
    print("----------------------------------------- ImgLinear")
    x=_b* _imgArray + _a
    imgout=Image.fromarray(x.astype(np.uint8))
    return imgout

def ImgInvers(_imgArray):
    print("----------------------------------------- ImgInvers")
    x=255- _imgArray
    imgout=Image.fromarray(x.astype(np.uint8))
    return imgout

def ImgLog(_imgArray):
    print("----------------------------------------- ImgLog")
    x = np.abs(np.log(_imgArray+1.1)*255 /
               np.log(np.max(_imgArray+1.1)))
    imgout=Image.fromarray(x.astype(np.uint8))
    return imgout

def marixRange(_imgArray,_min,_max):
    v1=(_max-_min)/255
    print(v1)
    for i in range(0,_imgArray.shape[0]):
        for j in range(0,_imgArray.shape[1]):
           if _imgArray[i][j] > _max :
              _imgArray[i][j] = 255
           elif _imgArray[i][j] < _min :
              _imgArray[i][j] = 0
           else:
              _imgArray[i][j]= _imgArray[i][j] * v1
    return _imgArray

def Hexencode(rgb):
    r=rgb[0]
    g=rgb[1]
    b=rgb[2]
    return '#%02x%02x%02x' % (r,g,b)

# ****************************************************************************

def ConvertMatrix_2d(_imgArray):
    print("----------------------------------------- ConvertMatrix_2d")
    if len(_imgArray.shape) == 2:
        n_line = _imgArray.shape[0]
        n_cols = _imgArray.shape[1]
        print("matrix 2 D","row",n_line,"col",n_cols)
        return _imgArray
    else:
        n_line = _imgArray.shape[0]
        n_cols = _imgArray.shape[1]
        n_3 = _imgArray.shape[2]
        print("matrix 3 D","row",n_line,"col",n_cols,"d_3",n_3)
        matrix2D = np.zeros((n_line,n_cols), np.uint64)
        for i in range(0,n_line):
            for j in range(0,n_cols):
                val= int((_imgArray[i,j,0]+_imgArray[i,j,1]+_imgArray[i,j,2])/3)
                matrix2D[i,j]= val
                
        return matrix2D

def ConvertImage_BiColor(_img,_seullage):
    print("----------------------------------------- ConvertImage_BiColor")
    # fn = lambda x : 255 if x > _seullage else 0
    # return _img.convert('L').point(fn, mode='1')
    mt = np.array(_img)
    mt_bi = np.where(mt > _seullage, 255, 0)
    return Image.fromarray(mt_bi.astype(np.uint8))
    
def ConvertMatrix_Image(_imgArray2d):
    print("----------------------------------------- ConvertMatrix_Image")
    imgout = Image.fromarray(_imgArray2d.astype(np.uint32))
    return imgout

def HistogramMatrix255 (_imgArray):
    from matplotlib.backends.backend_agg import FigureCanvas
    from matplotlib.figure import Figure
    print("----------------------------------------- matrixHistogram255")
    y = np.zeros(256, np.uint32)
    for i in range(0,_imgArray.shape[0]):
        for j in range(0,_imgArray.shape[1]):
            y[_imgArray[i,j]] += 1
    
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.subplots()
    ax.set_xlabel("value of pixel")
    ax.set_ylabel("nomber repitition")   
    ax.set_title('histogram')
    ax.plot(range(0,256),y,'black');

    canvas.draw()  
    return canvas.renderer.buffer_rgba();
