#Matted Video기반 라인드로잉 동영상 생성

import cv2
import numpy as np
import os
from os.path import isfile, join
import coherentLineDrawing

def makedirs(path): 
   try: 
        os.makedirs(path) 
   except OSError: 
       if not os.path.isdir(path): 
           raise

def start(sigcv,tauv):

    makedirs('./images/result')

    vidcap = cv2.VideoCapture('matted.mp4')
    def getFrame(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = vidcap.read()
        if hasFrames:

            # read image
            img = image
            # shrink image if its size is considerable (500?)
            shape = img.shape[:-1][::-1]
            if any(map(lambda sz: sz > 500, shape)):
                img = cv2.resize(img,
                    tuple(map(lambda sz: int(sz * 0.5), shape)))
            # run on this image and return edge map
            edge = coherentLineDrawing.run(
                img=img, sobel_size=3,
                etf_iter=4, etf_size=6,
                fdog_iter=4, sigma_c=sigcv, rho=0.997, sigma_m=3.0,
                tau=tauv
                # 0.3 / 0.947
            )
            # save result
            cv2.imwrite("./images/result/"+"image"+str(count)+".jpg", edge)     # save frame as JPG file

        return hasFrames

    sec = 0
    frameRate = 0.1 #//capture image in each second
    count=1
    success = getFrame(sec)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(sec)

    #영상으로 저장
    pathIn= './images/result/'
    pathOut = 'outVideo.avi'
    fps = 10
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
    #for sorting the file names properly
    files.sort(key = lambda x: int(x[5:-4]))
    size=0
    for i in range(len(files)):
        filename=pathIn + files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)    
        #inserting the frames into an image array
        frame_array.append(img)
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), 10, size) #fps, size
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()
