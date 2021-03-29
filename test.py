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
    
# ----------------------------------------- 
# 1 Egalisation d’histogramme = OK
# 2 Lissage des images = smoothing = OK
# 3 Amélioration du contraste = Contrast enhancement = OK
# 4 Segmentation par clustering OK
# 5 Opérations morphologiques = OK
# 6 Détecteur SIFT OK
# 7 Descripteur SIFT OK
# 8 Distance euclidienne OK
# ----------------------------------------- 

def main() -> None:
    print("----------------------------------------- red Image origine")
    path1 = 'images/001_1_1.bmp'
    # path1 = 'images/01.bmp'
    path2 = 'images/001_1_2.bmp'
    imgArray1 = fn.ReadImage2d_Array(path1)
    imgArray2 = fn.ReadImage2d_Array(path2)

    print("----------------------------------------- Egalisation d’histogramme  : Histogram origine")
    h1 = fn.Histogram_Array(imgArray1)
    Show_images([imgArray1,h1],"Histogram original picture")

    print("----------------------------------------- Lissage des images : Filter Show")
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

    imgOut = fn.Filter_Array(imgArray1,filter0)
    Show_images([imgArray1,imgOut],"Filter Moyen")
        
    imgOut = fn.Filter_Array(imgArray1,filte_h)
    Show_images([imgArray1,imgOut],"Filter Horizontal")
    
    imgOut = fn.Filter_Array(imgArray1,filte_v)
    Show_images([imgArray1,imgOut],"Filter vertical")
    
    print("----------------------------------------- Amélioration du contraste : Contrast Range")
    _min,_max = 30,220
    h1 = fn.Histogram_Array(imgArray1)
    imgOut = fn.ContrastRange_Array(imgArray1,_min,_max)
    h2 = fn.Histogram_Array(imgOut)
    Show_images([imgArray1,h1,imgOut,h2],"Histogram Contrast Range min:{0} | max:{1}".format(_min,_max) )
    
    
    print("----------------------------------------- Amélioration du contraste")
    imgOut1 = fn.ContrastLog_Array(imgArray1)
    imgOut2 = fn.ContrastLinear_Array(imgArray1,2,0)
    imgOut3 = fn.ContrastInvers_255_Array(imgArray1)
    Show_images([imgArray1,imgOut1,imgOut2,imgOut3],"Contrast Log Linear Invers")
    
    print("----------------------------------------- Segmentation par clustering")
    iris_x,iris_y,iris_r = fn.iris(imgArray1)
    pupil_x,pupil_y,pupil_r = fn.pupil(imgArray1)
    
    imgIris = fn.zeroExternalArray(imgArray1,iris_x,iris_y,iris_r)
    imgIrisPupil = fn.zeroInternalArray(imgIris,pupil_x, pupil_y, pupil_r)
    
    Show_images([imgArray1,imgIrisPupil] , "Segmentation iris pupil")
    
    print("----------------------------------------- Opérations morphologiques : BiColor")
    imgBiColor = fn.Convert_BiColor_Array(imgArray1,50) # select pupil with color black
    imgBiColorInverce = 1 - imgBiColor                  # select pupil with color white = بؤبؤ العين
    Show_images([imgArray1,imgBiColor,imgBiColorInverce] , " image Bi Color")
    
    kernel = np.array ([[0, 1, 1, 1, 0],
                        [1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1],
                        [0, 1, 1, 1, 0]], dtype = np.uint8)
    print("----------------------------------------- Opérations morphologiques :Erosion")    
    imgoutErosion = fn.Erosion_Array(imgBiColorInverce,kernel)
    Show_images([imgBiColorInverce,imgoutErosion] , "Erosion")
    
    print("----------------------------------------- Opérations morphologiques :Dilation")
    imgoutDilation =fn.Dilation_Array(imgBiColorInverce,kernel)
    Show_images([imgBiColorInverce,imgoutDilation] , "Dilation")

    
    print("----------------------------------------- SIFT : Matching Show")
    imgMatching , p= fn.GetMatchingImageValue_Array(imgArray1,imgArray2)
    Show_images([imgMatching],"matches found SIFT =: {0}".format(p))
    
main()