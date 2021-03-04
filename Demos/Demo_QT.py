from PyQt5 import QtWidgets, QtCore # import PyQt5 widgets
import sys
import  Main as test

import Demo_OpenCV_LiveVideo as dlv

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = test.Ui_Dialog()
    ui.setupUi(window)

    ui.OpenWebCam.clicked.connect(dlv.demo_Webcam)

    window.show()
    sys.exit(app.exec_())