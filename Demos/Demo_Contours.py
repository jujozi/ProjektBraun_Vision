import cv2 as cv
import sys
from src import VisionLib as vl
import numpy as np
import sqlite3 as sql
import time


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

def loadConfigContours(Modul, ConfigId, pathDB = 'configs/Config.db'):

    print('Connect to DB: ' + pathDB + '...', end=' ')
    try:
        con = sql.connect(pathDB)
        print('CONNECTED')
    except:
        print('FAILD')
        sys.exit()
    con.row_factory = sql.Row
    cur = con.cursor()
    print('Get Config of '+Modul+' ...', end='')

    cur.execute("SELECT*FROM %s WHERE ConfigID=%i" %(Modul, ConfigId))
    config = cur.fetchone()
    if config is None:
        print('FAILD')
        print('ConfigID not found')
        sys.exit()
    else:
        print("DONE")
    return config


def nothing(x):
    print(x)

class CONTOURS():
    def __init__(self,configID):
        print(self.__class__.__name__+': Initialize pipline')
        self.loadConfig(configID)

    def loadConfig(self,configID):
        Config = loadConfigContours('ContoursConfig', configID)

        #Config Gauss
        self.GaussianBlur_Enable = Config['GaussianBlur']
        self.GaussianBlur_ksize_x = Config['GaussianBlur_ksize_x']
        self.GaussianBlur_ksize_y = Config['GaussianBlur_ksize_y']
        self.GaussianBlur_sigma = Config['GaussianBlur_sigma']

        #config Canny
        self.Canny_Enable = Config['Canny']
        self.Canny_threshold1 = Config['Canny_threshold1']
        self.Canny_threshold2 = Config['Canny_threshold2']

        # config Dilate
        self.Dilate_Enable = Config['Dilate']
        self.Dilate_kernel = np.ones((Config['Dilate_kernel_x'], Config['Dilate_kernel_y']))
        self.Dilate_iterations = Config['Dilate_iterations']

        # config Erode
        self.Erode_Enable = Config['Erode']
        self.Erode_kernel = np.ones((Config['Erode_kernel_x'], Config['Erode_kernel_y']))
        self.Erode_iterations = Config['Erode_iterations']

        # config FindRechtangel
        self.FindRechtangel_mode = eval(Config['FindRechtangel_mode'])
        self.FindRechtangel_method = eval(Config['FindRechtangel_method'])
        self.FindRechtangel_minArea = Config['FindRechtangel_minArea']
        self.FindRechtangel_maxArea = Config['FindRechtangel_maxArea']

    def process(self, frame):
        # Pipline

        imgGray =  cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        imgBlur = self.GaussianBlur(imgGray)
        imgCann = self.Canny(imgBlur)
        imgDila = self.Dilate(imgCann)
        imgErod = self.Erode(imgDila)

        imgRect = self.FindRectangel(imgErod, frame)

        # Debug View
        imgDebug = vl.stackImages([[imgGray, imgBlur, imgCann], [imgDila, imgErod, imgRect[0]]], 1, lables=[['imgGray', 'imgBlur', 'imgCann'], ['imgDila', 'imgErod', 'imgRect']])
        cv.imshow("Display window", vl.ResizeWithAspectRatio(imgDebug, width=800))

        imgFinal = imgRect[0]
        return imgFinal

    def GaussianBlur(self, src):
        # https://docs.opencv.org/master/d4/d86/group__imgproc__filter.html#gaabe8c836e97159a9193fb0b11ac52cf1
        if self.GaussianBlur_Enable:
            ksize_x = self.GaussianBlur_ksize_x
            ksize_y = self.GaussianBlur_ksize_y
            ksize = (ksize_x, ksize_y)
            sigma = self.GaussianBlur_sigma
            return cv.GaussianBlur(src, ksize, sigma)
        else:
            return src

    def Canny(self, src):
        # https://docs.opencv.org/master/dd/d1a/group__imgproc__feature.html#ga2a671611e104c093843d7b7fc46d24af
        # https://docs.opencv.org/master/da/d22/tutorial_py_canny.html
        if self.Canny_Enable:
            threshold1 = self.Canny_threshold1
            threshold2 = self.Canny_threshold2
            return cv.Canny(src, threshold1, threshold2)
        else:
            return src

    def Dilate(self, src):
        if self.Dilate_Enable:
            kernel = self.Dilate_kernel
            iterations = self.Dilate_iterations
            return cv.dilate(src, kernel, iterations=iterations)
        else:
            return src

    def Erode(self, src):
        # https://docs.opencv.org/3.4/d4/d86/group__imgproc__filter.html#gaeb1e0c1033e3f6b891a25d0511362aeb
        if self.Erode_Enable:
            kernel = self.Erode_kernel
            iterations = self.Erode_iterations
            return cv.erode(src, kernel, iterations=iterations)

        else:
            return src

    def ErodeDebug(self):
        cv.namedWindow('ErodeDebug')
        cv.createTrackbar('Erode_iterations', 'ErodeDebug', self.Dilate_iterations, 10, nothing)

    def FindRectangel(self, src, frame):
        # https://docs.opencv.org/master/dd/d49/tutorial_py_contour_features.html
        mode =  self.FindRechtangel_mode # https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html#ga819779b9857cc2f8601e6526a3a5bc71
        method = self.FindRechtangel_method# https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html#ga4303f45752694956374734a03c54d5ff

        minArea = self.FindRechtangel_minArea
        maxArea = self.FindRechtangel_maxArea

        # https://docs.opencv.org/3.4/d3/dc0/group__imgproc__shape.html#ga17ed9f5d79ae97bd4c7cf18403e1689a
        image, contours, hierarchy = cv.findContours(src, mode, method)
        contoursFilterd = []
        contoursAprox = []
        for contor in contours:
            area = cv.contourArea(contor)
            if minArea<area<maxArea:
                contoursFilterd.append(contor)
                # https://docs.opencv.org/master/d3/dc0/group__imgproc__shape.html#ga0012a5fdaea70b8a9970165d98722b4c
                contoursAprox.append(cv.approxPolyDP(contor, cv.arcLength(contor, True)*0.05, True))
        #cv.drawContours(frame, contoursFilterd, -1, (0, 255, 0), 3)
        cv.drawContours(frame, contoursAprox, -1, (0, 0, 255), 1)
        return frame, contoursFilterd, hierarchy

if __name__ == '__main__':
    ConfigID = 7
    Contours = CONTOURS(ConfigID)

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera ")


    loadConfigTime = time.time()
    while True:
        currentTime = time.time()
        # Capture frame-by-frame
        ret, frame = cap.read()
        #if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        #frame =cv.imread('SAVEcrop.png')

        if  currentTime > loadConfigTime + 1:
            Contours.loadConfig(ConfigID)
            loadConfigTime = currentTime

        img = Contours.process(frame)
        cv.imshow('asd',img)

        k = cv.waitKey(20) & 0xFF
        if k == 27:
            cv.destroyAllWindows()
            cap.release()
            break
        elif k == ord("s"):
            cv.imwrite("SAVE.png", frame)
