from PIL import Image

from functions import ConvertImage_2d
from functions import ConvertImage_BiColor

from functions import ContrastRange
from functions import ContrastLog
from functions import ContrastInvers
from functions import ContrastLinear

from functions import GetMatchingImageValue

from functions import Histogram_Image

from functions import FilterImage

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
    h1 = Histogram_Image(_img)
    Show_images("Histogram",[_img,h1])
    
def ContrastInversShow(_img) -> None:
    imgOut = ContrastInvers(_img)
    Show_images("Contrast Invers",[_img,imgOut])
    
def ContrastLinearShow(_img) -> None:
    imgOut = ContrastLinear(_img,2,0)
    Show_images("Contrast Linear",[_img,imgOut])
    
def ContrastLogShow(_img) -> None:
    imgOut = ContrastLog(_img)
    Show_images("Contrast Log",[_img,imgOut])
    
def MatchingShow(_img1,_img2) -> None:
    imgMatching , p= GetMatchingImageValue(_img1,_img2)
    # print("matches found : %d" % (p))
    Show_images("matches found SIFT =: {0}".format(p),[imgMatching])
    
def ContrastRangShow(_img,_min,_max) -> None:
    h1 = Histogram_Image(_img)
    imgOut = ContrastRange(_img,_min,_max)
    h2 = Histogram_Image(imgOut)
    Show_images("Histogram Contrast Rang min:{0} | max:{1}".format(_min,_max) ,[_img,h1,imgOut,h2])
    
def FilterImageShow(_img) -> None:
    import numpy as np
    filte_v = np.array([[-1, 0, 1],
                      [-2, 0, 2],
                      [-1, 0, 1 ]
                      ])
    
    filte_h = np.array([[-1, -2, -1],
                      [0, 0, 0],
                      [1, 2, 1 ]
                      ])
    
    filter0 = np.array([[1 / 9, 1 / 9, 1 / 9],
                  [1 / 9, 1 / 9, 1 / 9],
                  [1 / 9, 1 / 9, 1 / 9]])

    imgOut = FilterImage(_img,filter0)
    Show_images("Filter Moyen",[_img,imgOut])
        
    imgOut = FilterImage(_img,filte_h)
    Show_images("Filter Horizontal",[_img,imgOut])
    
    imgOut = FilterImage(_img,filte_v)
    Show_images("Filter vertical",[_img,imgOut])
    
# ----------------------------------------- 
# 1 Egalisation d’histogramme = OK
# 2 Lissage des images = smoothing = OK
# 3 Amélioration du contraste = Contrast enhancement = OK
# 6 Détecteur SIFT OK
# 7 Descripteur SIFT OK
# 8 Distance euclidienne OK

# 4 Segmentation par clustering NON
# 5 Opérations morphologiques = 50/100
# ----------------------------------------- 


def main() -> None:
    print("----------------------------------------- red Image origine")
    path1 = 'images/001_1_1.bmp'
    path2 = 'images/001_1_2.bmp'
    img1 = ConvertImage_2d(Image.open(path1))
    img2 = ConvertImage_2d(Image.open(path2))
    
    print("----------------------------------------- Egalisation d’histogramme  : Histogram origine")
    HistogramShow(img1)
    print("----------------------------------------- Lissage des images : Filter Show")
    FilterImageShow(img1)
    print("----------------------------------------- Amélioration du contraste : Contrast Rang")
    ContrastRangShow(img1,0,50)
    print("----------------------------------------- Amélioration du contraste : Contrast Log")
    ContrastLogShow(img1)
    print("----------------------------------------- Amélioration du contraste : Contrast Linear")
    ContrastLinearShow(img1)
    print("----------------------------------------- Amélioration du contraste : Contrast Invers")
    ContrastInversShow(img1)
    print("----------------------------------------- Opérations morphologiques : Histogram BiColor")
    imgBiColor = ConvertImage_BiColor(img1,50)
    HistogramShow(imgBiColor)

    print("----------------------------------------- SIFT : Matching Show")
    MatchingShow(img1,img2)

    
main()