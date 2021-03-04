import cv2 as cv
from src import VisionLib as vl
import os
from cv2 import aruco
import xml.etree.ElementTree as ET

def findVideoDevices():
    devs = os.listdir('/dev')
    devsVideo = []
    for dev in devs:
        if dev.startswith('video'):
            devsVideo.append(dev)
            
    return devsVideo

def selectVideoDevice(dev):
    cap = cv.VideoCapture(dev)
    if not cap.isOpened():
        print("Cannot open camera " + str(dev))
        return -1
    return cap

def demo_Webcam():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()


    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        # Display the resulting frame
        StackedImages = vl.stackImages([[frame, gray], [hsv, gray]], 1.0,
                                       lables=[['Input', 'Grauwert'], ['hsv', 'Grauwert']])
        cv.imshow("StackedImages", StackedImages)
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

def detectMarker(gray):
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_1000)
    arucoParameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(
        gray, aruco_dict, parameters=arucoParameters)
    marker = aruco.drawDetectedMarkers(gray, corners)
    return marker




if __name__ == '__main__':
    # load configuration
    xmlFile = 'Default'
    CamName = 'Webcam'
    tree = ET.parse('../configs/'+xmlFile+'.xml')

    VideoXml = tree.findall('Video')
    for Video in VideoXml:
        if Video.attrib['Device'] == CamName:
            CamXmlAtrib = Video.attrib
            dev = int(CamXmlAtrib['adress'])
        else:
            print('Cam not configured')

    cap = cv.VideoCapture(dev)
    if not cap.isOpened():
        print("Cannot open camera " + str(dev))

    x1 = int(CamXmlAtrib['x1'])
    x2 = int(CamXmlAtrib['x2'])
    y1 = int(CamXmlAtrib['y1'])
    y2 = int(CamXmlAtrib['y2'])

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frameROI = frame[x1:y1, x2:y2]
        gray = cv.cvtColor(frameROI, cv.COLOR_BGR2GRAY)
        hsv = cv.cvtColor(frameROI, cv.COLOR_BGR2HSV)
        marker = detectMarker(gray)
        # Display the resulting frame
        StackedImages = vl.stackImages([[frameROI, gray], [hsv, marker]], 1.0,
                                       lables=[['Input', 'Grauwert'], ['hsv', 'Grauwert']])
        cv.imshow("StackedImages", StackedImages)
        k = cv.waitKey(20) & 0xFF
        if k == 27:
            break

    cap.release()
    cv.destroyAllWindows()
