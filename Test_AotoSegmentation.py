import numpy as np
from PIL import Image
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

# ---------------------------------------------------------------------- get list fils from dir
def FilesYield(_dir_path,_extension):
    import os
    for root, dirs, files in os.walk(os.path.abspath(_dir_path)): 
        for file in files:
            file = str(file)
            if file.endswith(_extension):
                yield os.path.join(root, file)     
def Files(_dir_path,_extension):
    return [f for f in FilesYield(_dir_path,_extension)]

# ---------------------------------------------------------------------- read image to array
def ReadImage2d_Array(_path):
    image = Image.open(_path)
    imgArray = np.array(image)  
    if len(imgArray.shape) == 2:
        return imgArray
    else:
        print("len(imgArray.shape):",len(imgArray.shape))
        return None

# ---------------------------------------------------------------------- run script        
def SegmentationListAndSave(_listFilse,_outPath):
    import os
    if not os.path.exists(_outPath):
        os.makedirs(_outPath)
    for f in _listFilse:
        imgArray = ReadImage2d_Array(f)   
        
        imgArray ,pupil,iris = Segmentation(imgArray)
    
        img = Image.fromarray(imgArray.astype(np.uint8))
        saveTo =_outPath+"/"+os.path.basename(f)
        img.save(saveTo)
        print("Save : ",saveTo)
        
listPath = Files('./Casia_xxx_1_x','.bmp')
SegmentationListAndSave(listPath,'./irisDatabase')
