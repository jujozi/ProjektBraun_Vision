import numpy as np
import cv2 as cv
from src import VisionLib as vl
from xml.dom import minidom
import copy
from datetime import datetime
import xml.etree.ElementTree as ET
import os

class setROI():
    def __init__(self, CamName, xmlFile):
        # Create Directory for ROI Config
        try:
            os.makedirs("../configs/" + xmlFile + '/' + CamName + "/roi")
        except(OSError):
            print('Faild to create Dir')
        else:
            print('Successfully created Dir')

        # Open XML Config file
        tree = ET.parse('../configs/' + xmlFile + '.xml')

        VideoXml = tree.findall('Video')
        for Video in VideoXml:
            if Video.attrib['Device'] == CamName:
                CamXmlAtrib = Video.attrib
            else:
                print('Cam not fond')

        cv.namedWindow('image')
        cv.setMouseCallback('image', self.callbackMous)

        self.roi = np.zeros(4, dtype=int)

        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")


        while np.isin(self.roi, 0).max():
            cv.imshow('image', frame)
            k = cv.waitKey(20) & 0xFF
            if k == 27:
                break

        print('ROI set')
        cv.setMouseCallback('image', self.callbackMousDisable)

        date = datetime.now()
        CamXmlAtrib['x1'] = str(self.roi[1])
        CamXmlAtrib['x2'] = str(self.roi[0])
        CamXmlAtrib['y1'] = str(self.roi[3])
        CamXmlAtrib['y2'] = str(self.roi[2])
        CamXmlAtrib['Date'] = date.strftime("%d/%m/%Y %H:%M:%S")
        tree.write('../configs/' + xmlFile + '.xml')

        frameRectangel = copy.deepcopy(frame)

        while 1:
            cv.imshow('image', frameRectangel)
            cv.rectangle(frameRectangel, (self.roi[0], self.roi[1]), (self.roi[2], self.roi[3]), (0, 255, 0), 3)
            cropROI = frame[self.roi[1]:self.roi[3], self.roi[0]:self.roi[2]]
            cv.imshow('cropROI', cropROI)
            k = cv.waitKey(20) & 0xFF
            if k == 27:
                break
        cv.imwrite("../configs/" + xmlFile + '/' + CamName + "/roi/Overviwe.jpg", frame)
        cv.imwrite("../configs/" + xmlFile + '/' + CamName + "/roi/Crop.jpg", cropROI)
        cv.destroyWindow('image')
        cv.destroyWindow('cropROI')



    def callbackMous(self,event,x,y,flags,param):
        if event == cv.EVENT_LBUTTONDBLCLK:
            self.roi[0] = x
            self.roi[1] = y
        if event == cv.EVENT_RBUTTONDBLCLK:
            self.roi[2] = x
            self.roi[3] = y

    def callbackMousDisable(self, event, x, y, flags, param):
        return 1

    def getROI(self):
        return self.roi

if __name__ == '__main__':
    setROI('Webcam', 'Default')
