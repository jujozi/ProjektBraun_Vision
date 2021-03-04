# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(413, 319)
        self.OpenWebCam = QtWidgets.QPushButton(Dialog)
        self.OpenWebCam.setGeometry(QtCore.QRect(10, 10, 100, 27))
        self.OpenWebCam.setObjectName("OpenWebCam")
        self.OpenSlider = QtWidgets.QPushButton(Dialog)
        self.OpenSlider.setGeometry(QtCore.QRect(120, 10, 100, 27))
        self.OpenSlider.setObjectName("OpenSlider")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(230, 10, 100, 27))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.OpenWebCam.setText(_translate("Dialog", "PushButton"))
        self.OpenSlider.setText(_translate("Dialog", "PushButton"))
        self.pushButton_3.setText(_translate("Dialog", "PushButton"))

