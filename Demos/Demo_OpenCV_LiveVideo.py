import cv2 as cv
from src import VisionLib as vl
import os
from cv2 import aruco
import xml.etree.ElementTree as ET
import copy
import numpy as np
import time

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
    return corners, ids, rejectedImgPoints

def calibrate_camera(allCorners,allIds,imsize):
    """
    Calibrates the camera using the dected corners.
    """
    print("CAMERA CALIBRATION")
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    board = aruco.CharucoBoard_create(7, 6, 1, .8, aruco_dict)

    cameraMatrixInit = np.array([[ 1000.,    0., imsize[0]/2.],
                                 [    0., 1000., imsize[1]/2.],
                                 [    0.,    0.,           1.]])

    distCoeffsInit = np.zeros((5,1))
    retval, cameraMatrix, distCoeffs, rvecs, tvecs = cv.aruco.calibrateCameraCharuco(allCorners, allIds, board, imsize, cameraMatrixInit, distCoeffsInit)

    return cameraMatrix, distCoeffs

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

    calib = False
    camera_matrix = 0
    distortion_coefficients0 = 0

    count = 0
    allCorners = []
    allIds = []
    lastTime = 0
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    board = aruco.CharucoBoard_create(7, 6, 1, .8, aruco_dict)

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

        # Marker detection
        corners, ids, rejectedImgPoints = detectMarker(gray)
        marker = copy.deepcopy(frameROI)
        marker = aruco.drawDetectedMarkers(marker, corners, ids=ids )


        # Display the resulting frame
        StackedImages = vl.stackImages([[frameROI, gray], [hsv, marker]], 1.0,
                                       lables=[['Input', 'Grauwert'], ['hsv', 'Grauwert']])
        cv.imshow("StackedImages", StackedImages)

        if calib == False and isinstance(ids, np.ndarray) and isinstance(corners, list):
            if ids.shape[0] == len(corners) and len(corners) == 21:
                if time.time() > lastTime+1:
                    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.00001)
                    # SUB PIXEL DETECTION
                    for corner in corners:
                        cv.cornerSubPix(gray, corner,
                                         winSize=(3, 3),
                                         zeroZone=(-1, -1),
                                         criteria=criteria)
                    res2 = cv.aruco.interpolateCornersCharuco(corners, ids, gray, board)
                    if res2[1] is not None and res2[2] is not None and len(res2[1]) > 3:
                        allCorners.append(res2[1])
                        allIds.append(res2[2])
                        count+= 1
                        lastTime = time.time()
                        print('Add calib'+str(count))

        if count>40 and calib != True:
            imsize = gray.shape
            camera_matrix, distortion_coefficients0 = calibrate_camera(allCorners, allIds, imsize)
            print(distortion_coefficients0)
            print(camera_matrix)
            calib = True

        if calib == True:
            position = aruco.estimatePoseSingleMarkers(corners, 0.0094, camera_matrix, distortion_coefficients0)
            print(position)
        k = cv.waitKey(20) & 0xFF
        if k == 27:
            break
        elif k == ord("s"):
            cv.imwrite("SAVE.png", img)

    cap.release()
    cv.destroyAllWindows()
