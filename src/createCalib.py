import os
import sqlite3 as sql
import cv2 as cv
from cv2 import aruco
import sys
import time
import numpy as np

import VisionLib as vl


class getFrames():
    def __init__(self):
        print(self.__class__.__name__+': Initialize...')
        self.dev = None
        self.cap = None
        self.Sequence_ID = 1
        self.con, self.cur = self.createDB()

        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.board = aruco.CharucoBoard_create(7, 6, 1, .8, aruco_dict)

    def createDB(self):
        # check if DB exist
        pathDB = 'configs/Calibration.db'
        print(self.__class__.__name__+': Check database '+pathDB+' ...', end='')
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
            print(self.__class__.__name__+': Create DB ...', end='')
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
                        '[Board] BLOB )')

            cur.execute('CREATE TABLE Calib ([Calib_ID] INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, '
                        '[Camera_ID] TEXT, '
                        '[Sequence_ID] INTEGER )')
        return con, con


    def openCam(self, dev):
        self.dev = dev
        print(self.__class__.__name__ + ': Open Cam '+str(dev)+' ...', end='')
        self.cap = cv.VideoCapture(1)
        if not self.cap.isOpened():
            print("FAILD")
            sys.exit()
        else:
            print('OK')

        print(self.__class__.__name__ + ': Enter stream loop ...')
        print('')
        print(self.__class__.__name__ + ': Press "ESC" to exit')
        print(self.__class__.__name__ + ': Press "s" to save frame to calibration db')
        while True:
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            date = time.time()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            cv.imshow('Calibration', frame)
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

class Calibrate():
    def __init__(self):
        print(self.__class__.__name__ + ': Initialize...')
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.board = aruco.CharucoBoard_create(7, 6, 1, .8, aruco_dict)


        # check if DB exist
        pathDB = 'configs/Calibration.db'
        print(self.__class__.__name__ + ': Check database ' + pathDB + ' ...', end='')
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



    def getMarker(self, Sequence_ID):
        print(self.__class__.__name__ + ': Detect Marker ...')
        cur = self.con.cursor()
        cur.execute("SELECT Frame FROM Frames WHERE Sequence_ID='%i'" % (Sequence_ID,))


        allCorners = []
        allIds = []

        allBFrames = cur.fetchall()
        for BFrame in allBFrames:
            npFrame = np.frombuffer(BFrame[0], np.uint8)
            frame = cv.imdecode(npFrame, cv.IMREAD_COLOR)
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            corners, ids, rejectedImgPoints = vl.detectMarker(gray)

            if isinstance(ids, np.ndarray) and isinstance(corners, list):
                if ids.shape[0] == len(corners) and len(corners) == 21:
                    print('juhe')
                    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.00001)
                    # SUB PIXEL DETECTION
                    for corner in corners:
                        cv.cornerSubPix(gray, corner,
                                        winSize=(3, 3),
                                        zeroZone=(-1, -1),
                                        criteria=criteria)
                    res2 = cv.aruco.interpolateCornersCharuco(corners, ids, gray, self.board)
                    if res2[1] is not None and res2[2] is not None and len(res2[1]) > 3:
                        allCorners.append(res2[1])
                        allIds.append(res2[2])

        imsize = gray.shape

        camera_matrix, distortion_coefficients0 = self.calibrate_camera(allIds, allCorners, imsize)

        print(camera_matrix)
        print(distortion_coefficients0)

        return 1

    def calibrate_camera(self, allCorners, allIds, imsize):
        """
        Calibrates the camera using the dected corners.
        """
        print("CAMERA CALIBRATION")

        cameraMatrixInit = np.array([[1000., 0., imsize[0] / 2.],
                                     [0., 1000., imsize[1] / 2.],
                                     [0., 0., 1.]])

        distCoeffsInit = np.zeros((5, 1))
        retval, cameraMatrix, distCoeffs, rvecs, tvecs = cv.aruco.calibrateCameraCharuco(allCorners, allIds, self.board,
                                                                                         imsize, cameraMatrixInit,
                                                                                         distCoeffsInit)

        return retval, cameraMatrix, distCoeffs, rvecs, tvecs



if __name__ == '__main__':
    Frames = getFrames()
    Frames.createDB()
    Frames.openCam(0)

    Calib = Calibrate()
    Calib.getMarker(1)

    sys.exit()
