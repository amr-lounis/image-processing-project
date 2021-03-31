import functions as fn

def FilesYield(_dir_path,_extension):
    import os
    for root, dirs, files in os.walk(os.path.abspath(_dir_path)): 
        for file in files:
            file = str(file)
            if file.endswith(_extension):
                yield os.path.join(root, file)     
def Files(_dir_path,_extension):
    return [f for f in FilesYield(_dir_path,_extension)]

def SegmentationListAndSave(_listFilse,_outPath):
    import os
    if not os.path.exists(_outPath):
        os.makedirs(_outPath)
    for f in _listFilse:
        imgArray = fn.ReadImage2d_Array(f)   
        
        imgArray ,pupil,iris = fn.Segmentation(imgArray)
    
        img = fn.Convert_Array2Image(imgArray)
        saveTo =_outPath+"/"+os.path.basename(f)
        img.save(saveTo)
        print("Save : ",saveTo)
        
listPath = Files('./Casia_xxx_1_x','.bmp')
SegmentationListAndSave(listPath,'./Casia_Segmentation')
