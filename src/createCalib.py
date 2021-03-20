import os
import sqlite3 as sql
import cv2 as cv
from cv2 import aruco
import sys
import time
import numpy as np
import pickle

import copy

import VisionLib as vl


class getFrames():
    def __init__(self):
        print(self.__class__.__name__+': Initialize... ')
        self.dev = None
        self.cap = None
        self.Sequence_ID = 1
        self.con, self.cur = self.createDB()

        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.board = aruco.CharucoBoard_create(7, 6, 1, .8, aruco_dict)

    def createDB(self):
        # check if DB exist
        pathDB = 'configs/Calibration.db'
        print(self.__class__.__name__+': Check database '+pathDB+' ... ', end='')
        if os.path.exists(pathDB):
            print('exist')
            print(self.__class__.__name__ + ': Connect to DB ... ', end='')
            try:
                con = sql.connect(pathDB)
                print('OK')
            except:
                print('FAILD')
                sys.exit()
        else:
            print('not found')
            # Create new DB
            print(self.__class__.__name__+': Create DB ... ', end='')
            try:
                con = sql.connect(pathDB)
                print('OK')
            except:
                print('FAILD')
            print(self.__class__.__name__+': Create Tables', end='')
            cur = con.cursor()
            cur.execute('CREATE TABLE Frames ([Frame_ID] INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, '
                        '[Sequence_ID] INTEGER, '
                        '[Date] INTEGER,'
                        '[Camera_ID] TEXT,'
                        '[Frame] BLOB ,'
                        '[Corners] BLOB,'
                        '[Ids] BLOB,'
                        '[Board] BLOB )')

            cur.execute('CREATE TABLE Calib ([Calib_ID] INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, '
                        '[Camera_ID] TEXT, '
                        '[retval] REAL, '
                        '[cameraMatrix] BLOB, '
                        '[distCoeffs] BLOB, '
                        '[rvecs] BLOB, '
                        '[tvecs] BLOB, '
                        '[Sequence_ID] INTEGER )')
        return con, con

    def autoCapture(self, dev):
        print(self.__class__.__name__ + ': Start auto capturing')
        print(self.__class__.__name__ + ': Connect to video device '+str(dev), end='')
        cap = cv.VideoCapture(dev)
        if not cap.isOpened():
            print("Cannot open camera " + str(dev))
            sys.exit()
        print('CONNECTED')
        print(self.__class__.__name__ + ': Enter stream loop ... ')
        print('')
        print('Frames witch show all markers will be automatically added to the database')

        lastTime = 0
        count = 0
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            date = time.time()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ... ")
                break
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            # Marker detection
            corners, ids, rejectedImgPoints = detectMarker(gray)

            if isinstance(ids, np.ndarray) and isinstance(corners, list):
                if ids.shape[0] == len(corners) and len(corners) == 21:
                    if time.time() > lastTime + 1:
                        lastTime = time.time()
                        count += 1
                        print('Add calib' + str(count))
                        self.saveFrame(frame, date)
                        frame = aruco.drawDetectedMarkers(frame, corners, ids=ids)


            cv.imshow("StackedImages", frame)
            k = cv.waitKey(20) & 0xFF
            if k == 27:
                break

    def openCam(self, dev):
        self.dev = dev
        print(self.__class__.__name__ + ': Open Cam '+str(dev)+' ... ', end='')
        self.cap = cv.VideoCapture(dev)
        if not self.cap.isOpened():
            print("FAILD")
            sys.exit()
        else:
            print('OK')

        print(self.__class__.__name__ + ': Enter stream loop ... ')
        print('')
        print(self.__class__.__name__ + ': Press "ESC" to exit')
        print(self.__class__.__name__ + ': Press "s" to save frame to calibration db')
        while True:
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            date = time.time()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ... ")
                break
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = vl.detectMarker(gray)
            frame_Marker = aruco.drawDetectedMarkers(frame, corners)
            cv.imshow('Calibration', frame_Marker)
            k = cv.waitKey(20) & 0xFF
            if k == 27:
                cv.destroyWindow('Calibration')
                self.cur.close()
                self.con.close()
                self.cap.release()
                break
            if k == ord('s'):
                print(self.__class__.__name__ + ': Save frame')
                self.saveFrame(frame, date)

    def saveFrame(self, frame, date):
        retval, buf	 = cv.imencode('.png', frame)
        self.cur.execute(' INSERT INTO Frames (Sequence_ID, Date, Camera_ID, Frame) VALUES (?, ?, ?, ?)',(self.Sequence_ID, date, self.dev, buf))
        self.con.commit()

def detectMarker(gray):
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_1000)
    arucoParameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(
        gray, aruco_dict, parameters=arucoParameters)
    return corners, ids, rejectedImgPoints

class Calibrate():
    def __init__(self):
        print(self.__class__.__name__ + ': Initialize... ')
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.board = aruco.CharucoBoard_create(7, 6, 1, .8, aruco_dict)


        # check if DB exist
        pathDB = 'configs/Calibration.db'
        print(self.__class__.__name__ + ': Check database ' + pathDB + ' ... ', end='')
        if os.path.exists(pathDB):
            print('exist')
            print(self.__class__.__name__ + ': Connect to DB ... ', end='')
            try:
                self.con = sql.connect(pathDB)
                print('OK')
            except:
                print('FAILD')
                sys.exit()
        else:
            print('not found')
            sys.exit()


    def displayFrame(self,frame_id):
        print(self.__class__.__name__ + ': display Frame')
        cur = self.con.cursor()
        cur.execute("SELECT Frame FROM Frames WHERE Sequence_ID='%i'" % (1,))
        Frames = cur.fetchall()
        for BFrame in Frames:
            npFrame = np.frombuffer(BFrame[0], np.uint8)
            frame = cv.imdecode(npFrame, cv.IMREAD_COLOR)
            while True:
                cv.imshow('Calibration', frame)
                k = cv.waitKey(20) & 0xFF
                if k == 27:
                    cv.destroyWindow('Calibration')
                    break



    def getMarker(self, Sequence_ID):
        print(self.__class__.__name__ + ': Initialize camera Calibration ... ', end='')
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        board = aruco.CharucoBoard_create(7, 6, 1, .8, aruco_dict)

        allCorners = []
        allIds = []

        print('DONE')

        print(self.__class__.__name__ + ': Get frames from sequence id: '+str(Sequence_ID)+' ... ', end='')
        cur = self.con.cursor()
        cur.execute("SELECT Frame FROM Frames WHERE Sequence_ID='%i'" % (Sequence_ID,))
        allBFrames = cur.fetchall()
        print('DONE')

        print(self.__class__.__name__ + ': Extract marker ... ', end='')
        for BFrame in allBFrames:
            npFrame = np.frombuffer(BFrame[0], np.uint8)
            frame = cv.imdecode(npFrame, cv.IMREAD_COLOR)
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = detectMarker(gray)
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
        print('DONE')
        print(self.__class__.__name__ + ': found '+str(len(allIds))+' frames with markers')


        imsize = gray.shape
        retval, cameraMatrix, distCoeffs, rvecs, tvecs = self.calibrate_camera(allCorners, allIds, imsize)

        return 1

    def calibrate_camera(self, allCorners, allIds, imsize):
        """
        Calibrates the camera using the dected corners.
        """
        print(self.__class__.__name__ + ': Initialize calibration ... ', end='')

        cameraMatrixInit = np.array([[1000., 0., imsize[0] / 2.],
                                     [0., 1000., imsize[1] / 2.],
                                     [0., 0., 1.]])

        distCoeffsInit = np.zeros((5, 1))
        print('DONE')
        print(self.__class__.__name__ + ': Start calibration calculations ... ', end='')
        retval, cameraMatrix, distCoeffs, rvecs, tvecs = cv.aruco.calibrateCameraCharuco(allCorners, allIds, self.board,
                                                                                         imsize, cameraMatrixInit,
                                                                                         distCoeffsInit)
        print('DONE')

        print(self.__class__.__name__ + ': Write results to database ... ', end='')

        Camera_ID = int(0)
        Sequence_ID = 1

        cameraMatrix_b = cameraMatrix.tobytes()
        distCoeffs_b = distCoeffs.tobytes()
        rvecs_b = bytes()
        tvecs_b = bytes()

        cur = self.con.cursor()
        cur.execute(' INSERT INTO Calib (Camera_ID, retval, cameraMatrix, distCoeffs, rvecs, tvecs, Sequence_ID) VALUES (?, ?, ?, ?, ?, ?, ?)',(Camera_ID, retval, cameraMatrix_b, distCoeffs_b, rvecs_b, tvecs_b, Sequence_ID))
        self.con.commit()
        print('DONE')

        return retval, cameraMatrix, distCoeffs, rvecs, tvecs

    def getCalib(self,Calib_ID):
        print(self.__class__.__name__ + ': Get calibration data ... ', end='')

        cur = self.con.cursor()
        cur.execute("SELECT cameraMatrix FROM Calib WHERE Calib_ID='%i'" % (Calib_ID,))
        print('DONE')
        cameraMatrix_b = cur.fetchone()[0]
        cameraMatrix = np.frombuffer(cameraMatrix_b)
        print(cameraMatrix)



if __name__ == '__main__':
    #Frames = getFrames()
    #Frames.createDB()
    #Frames.openCam(0)
    #Frames.autoCapture(0)

    Calib = Calibrate()
    Calib.getMarker(1)
    Calib.getCalib(1)

    sys.exit()
