import numpy as np
from PIL import Image
from functions import HistogramMatrix255
from functions import ConvertMatrix_2d
from functions import ConvertMatrix_Image
from functions import ConvertImage_BiColor

from functions import ImgInvers
from functions import ImgLinear
from functions import ImgLog

from functions import getMatchingNumber

def Show_images(_title,_list) -> None:
    import matplotlib.pyplot as plt
    n: int = len(_list)
    f =  plt.figure(figsize=(10,5))
    f.suptitle(_title, fontsize=16)
    for i in range(n):
        # Debug, plot figure
        f.add_subplot(1, n, i + 1)
        plt.axis('off')
        plt.imshow(_list[i],cmap='gray')
        
    plt.show(block=True)

def HistogramShow(_img) -> None:
    imgMarix2D = np.array(_img)
    matrix2D = ConvertMatrix_2d(imgMarix2D)
    h1 = HistogramMatrix255(matrix2D)
    img = ConvertMatrix_Image(matrix2D)
    Show_images("Histogram",[img,h1])
    
def inversColorShow(_img) -> None:
    imgMarix2D = np.array(_img)
    matrix2D = ConvertMatrix_2d(imgMarix2D)
    imgOut = ImgInvers(matrix2D)
    Show_images("invers Color",[_img,imgOut])
    
def linearShow(_img) -> None:
    imgMarix2D = np.array(_img)
    matrix2D = ConvertMatrix_2d(imgMarix2D)
    imgOut = ImgLinear(matrix2D,0.2,0)
    Show_images("linear",[_img,imgOut])
    
def logShow(_img) -> None:
    imgMarix2D = np.array(_img)
    matrix2D = ConvertMatrix_2d(imgMarix2D)
    imgOut = ImgLog(matrix2D)
    Show_images("log",[_img,imgOut])
    
def matchingShow(_path1,_path2) -> None:
    imgMatching , p= getMatchingNumber(_path1,_path2)
    # print("matches found : %d" % (p))
    Show_images("matches found SIFT =: {0}".format(p),[imgMatching])
    
# ----------------------------------------- 
# 1 Egalisation d’histogramme = OK
# 3 Amélioration du contraste = Contrast enhancement = OK
# 6 Détecteur SIFT OK
# 7 Descripteur SIFT OK
# 8 Distance euclidienne OK

# 2 Lissage des images = smoothing = NON
# 4 Segmentation par clustering OK
# 5 Opérations morphologiques NON 50/100
# ----------------------------------------- 

def main():
    print("----------------------------------------- redImage origine")
    path1 = 'Images/001_1_1.bmp'
    path2 = 'Images/001_1_2.bmp'
    img1 = Image.open(path1)
    img2 = Image.open(path2)
    # 
    logShow(img1)
    # 
    linearShow(img1)
    # image inverce
    inversColorShow(img1)
    # Histograme
    HistogramShow(img1)
    # bi color
    imgBiColor = ConvertImage_BiColor(img1,50)
    HistogramShow(imgBiColor)
    # 
    matchingShow(img1,img2)
main()
