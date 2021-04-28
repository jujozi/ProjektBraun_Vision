#!/usr/bin/python

from PyQt5.QtWidgets import (QWidget, QSlider, QHBoxLayout, QPushButton,
                             QLabel, QApplication, QVBoxLayout, QCheckBox, QLineEdit, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import sys
import sqlite3 as sql
from src import createCalib

class gui():
    def __init__(self):
        print(self.__class__.__name__ + ': Initialize GUI... ')

        self.window = QWidget()
        self.window.setLayout(self.calibButton())
        self.window.show()

        self.Frames = createCalib.getFrames()
        self.Frames.createDB()

        self.Calib = createCalib.Calibrate()


    def calibButton(self):
        layout = QVBoxLayout()

        subLayoutCaminput = QHBoxLayout()

        labelCamInput = QLabel('Cam Id')
        textCamInput = QLineEdit('0')
        buttonCamInput = QPushButton("Open")
        buttonCamInput.clicked.connect(lambda: self.Frames.openCam(int(textCamInput.text())))

        subLayoutCaminput.addWidget(labelCamInput)
        subLayoutCaminput.addWidget(textCamInput)
        subLayoutCaminput.addWidget(buttonCamInput)
        layout.addLayout(subLayoutCaminput)

        subLayoutAutoCalib = QHBoxLayout()

        labelAutoCalib = QLabel('Sequence ID')
        textAutoCalib = QLineEdit('0')
        buttonAutoCalib = QPushButton("Auto Capture Calibration")
        buttonAutoCalib.setCheckable(True)
        buttonAutoCalib.clicked.connect(lambda:  self.Frames.autoCapture(int(textAutoCalib.text())))

        subLayoutAutoCalib.addWidget(labelAutoCalib)
        subLayoutAutoCalib.addWidget(textAutoCalib)
        subLayoutAutoCalib.addWidget(buttonAutoCalib)
        layout.addLayout(subLayoutAutoCalib)

        subLayoutComputeCalib = QHBoxLayout()

        labeComputeCalib = QLabel('Sequence ID')
        textComputeCalib = QLineEdit('0')
        buttonComputeCalib= QPushButton('Start Calibration')
        buttonComputeCalib.setCheckable(True)
        buttonComputeCalib.clicked.connect(lambda: self.Calib.getMarker(int(textComputeCalib.text())))

        subLayoutComputeCalib.addWidget(labeComputeCalib)
        subLayoutComputeCalib.addWidget(textComputeCalib)
        subLayoutComputeCalib.addWidget(buttonComputeCalib)
        layout.addLayout(subLayoutComputeCalib)

        subLayoutShowUndist= QHBoxLayout()

        labeShowUndist = QLabel('Calib ID')
        textShowUndist = QLineEdit('0')
        buttonShowUndist = QPushButton('Start Undist view')
        buttonShowUndist.setCheckable(True)
        buttonShowUndist.clicked.connect(lambda: self.Frames.showUndistorted(int(textShowUndist.text())))

        subLayoutShowUndist.addWidget(labeShowUndist)
        subLayoutShowUndist.addWidget(textShowUndist)
        subLayoutShowUndist.addWidget(buttonShowUndist)
        layout.addLayout(subLayoutShowUndist)



        return layout


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = gui()
    sys.exit(app.exec_())