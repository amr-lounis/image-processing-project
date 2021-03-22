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