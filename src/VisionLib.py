import cv2 as cv
import numpy as np

def selInput():

    return

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv.resize(image, dim, interpolation=inter)

def stackImages(imgArray,scale,lables=[]):
    sizeW= imgArray[0][0].shape[1]
    sizeH = imgArray[0][0].shape[0]
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv.resize(imgArray[x][y], (sizeW, sizeH), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv.cvtColor( imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv.resize(imgArray[x], (sizeW, sizeH), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        for d in range(0, rows):
            for c in range (0,cols):
                cv.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv.FILLED)
                cv.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver

class setROI():
    def __init__(self, frame, config):

        tree = minidom.parse("../configs/"+config+".xml")


        self.roi = np.zeros(4)

        cv.namedWindow('image')
        cv.setMouseCallback('image', self.callbackMous)


        while np.isin(self.roi, 0).max():
            cv.imshow('image', frame)
            k = cv.waitKey(20) & 0xFF
            if k == 27:
                break

        while 1:
            cv.imshow('image', frame)
            k = cv.waitKey(20) & 0xFF
            if k == 27:
                break
            cv.rectangle(frame, (self.roi[0], self.roi[1]), (self.roi[2], self.roi[3]), (0, 255, 0), 3)


    def callbackMous(self,event,x,y,flags,param):
        if event == cv.EVENT_LBUTTONDBLCLK:
            cv.circle(frame, (x, y), 100, (255, 0, 0), -1)
            self.roi[0] = x
            self.roi[1] = y
        if event == cv.EVENT_RBUTTONDBLCLK:
            cv.circle(frame, (x, y), 100, (255, 0, 0), -1)
            self.roi[2] = x
            self.roi[3] = y