from PIL import Image
import numpy as np
import functions as fn

def Show_images(_list,_title="") -> None:
    import matplotlib.pyplot as plt
    n: int = len(_list)
    f =  plt.figure(figsize=(5*len(_list),5))
    f.suptitle(_title, fontsize=16)
    for i in range(n):
        f.add_subplot(1, n, i + 1)
        plt.axis('off')
        plt.imshow(_list[i],cmap='gray')
    
    plt.show(block=True)
    
def HistogramShow(_img,_of="") -> None:
    h1 = fn.Histogram_Image(_img)
    Show_images([_img,h1],"Histogram "+ _of)
    
def ContrastShow(_img) -> None:
    imgOut = fn.ContrastLog(_img)
    Show_images([_img,imgOut],"Contrast Log")
    
    imgOut = fn.ContrastLinear(_img,2,0)
    Show_images([_img,imgOut],"Contrast Linear")
    
    imgOut = fn.ContrastInvers_255(_img)
    Show_images([_img,imgOut],"Contrast Invers")
    
def MatchingShow(_img1,_img2) -> None:
    imgMatching , p= fn.GetMatchingImageValue(_img1,_img2)
    # print("matches found : %d" % (p))
    Show_images([imgMatching],"matches found SIFT =: {0}".format(p))
    
def ContrastRangeShow(_img,_min,_max) -> None:
    h1 = fn.Histogram_Image(_img)
    imgOut = fn.ContrastRange(_img,_min,_max)
    h2 = fn.Histogram_Image(imgOut)
    Show_images([_img,h1,imgOut,h2],"Histogram Contrast Range min:{0} | max:{1}".format(_min,_max) )
    
def FilterImageShow(_img) -> None:

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

    imgOut = fn.FilterImage(_img,filter0)
    Show_images([_img,imgOut],"Filter Moyen")
        
    imgOut = fn.FilterImage(_img,filte_h)
    Show_images([_img,imgOut],"Filter Horizontal")
    
    imgOut = fn.FilterImage(imgOut,filte_v)
    Show_images([_img,imgOut],"Filter vertical")
    
# ----------------------------------------- 
# 1 Egalisation d’histogramme = OK
# 2 Lissage des images = smoothing = OK
# 3 Amélioration du contraste = Contrast enhancement = OK
# 5 Opérations morphologiques = OK
# 6 Détecteur SIFT OK
# 7 Descripteur SIFT OK
# 8 Distance euclidienne OK

# 4 Segmentation par clustering NON
# ----------------------------------------- 

def main() -> None:
    print("----------------------------------------- red Image origine")
    path1 = 'images/001_1_1.bmp'
    # path1 = 'images/01.bmp'
    path2 = 'images/001_1_2.bmp'
    img1 = fn.ConvertImage_2d(Image.open(path1))
    img2 = fn.ConvertImage_2d(Image.open(path2))
    
    print("----------------------------------------- Egalisation d’histogramme  : Histogram origine")
    HistogramShow(img1 , "original picture")
    # print("----------------------------------------- Lissage des images : Filter Show")
    # FilterImageShow(img1)
    # print("----------------------------------------- Amélioration du contraste : Contrast Range")
    # ContrastRangeShow(img1,30,220)
    # print("----------------------------------------- Amélioration du contraste")
    # ContrastShow(img1)
    # print("----------------------------------------- Opérations morphologiques : Histogram BiColor")
    imgBiColor = fn.ConvertImage_BiColor(img1,60) # select pupil with color black = بؤبؤ العين
    imgBiColor = fn.ContrastInvers_BiC(imgBiColor) 
    HistogramShow(imgBiColor , " image Bi Color")
    
    kernel = np.array ([[0, 1, 1, 1, 0],
                        [1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1],
                        [0, 1, 1, 1, 0]], dtype = np.uint8)
    print("----------------------------------------- Opérations morphologiques :Erosion")
    imgoutErosion =fn.ErosionImage(imgBiColor,kernel)
    HistogramShow(imgoutErosion , " Erosion")
    print("----------------------------------------- Opérations morphologiques :Dilation")
    imgoutDilation =fn.DilationImage(imgBiColor,kernel)
    HistogramShow(imgoutDilation , " Dilation")
    
    # print("----------------------------------------- SIFT : Matching Show")
    # MatchingShow(img1,img2)

    
main()