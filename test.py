import numpy as np
from PIL import Image
from functions import HistogramMatrix255
from functions import ConvertMatrix_2d
from functions import ConvertMatrix_Image
from functions import ConvertImage_BiColor

from functions import getMatchingNumber

def Show_images(_list) -> None:
    import matplotlib.pyplot as plt
    print("----------------------------------------- show_images")
    n: int = len(_list)
    f =  plt.figure(figsize=(10,20))
    for i in range(n):
        # Debug, plot figure
        f.add_subplot(1, n, i + 1)
        plt.axis('off')
        plt.imshow(_list[i],cmap='gray')
    plt.show(block=True)

def HistogramShow(_img):
    imgMarix2D = np.array(_img)
    matrix2D = ConvertMatrix_2d(imgMarix2D)
    h1 = HistogramMatrix255(matrix2D)
    img = ConvertMatrix_Image(matrix2D)
    Show_images([img,h1])
    
    
def main():
    print("----------------------------------------- redImage origine")
    path1 = 'Images/001_1_1.bmp'
    path2 = 'Images/001_1_2.bmp'
    img1 = Image.open(path2)
    HistogramShow(img1)
    # bi color
    imgBiColor = ConvertImage_BiColor(img1,50)
    HistogramShow(imgBiColor)
    # 
    imgMatching , p= getMatchingNumber(path1,path2)
    print("matches found : %d" % (p))
    Show_images([imgMatching])

main()
