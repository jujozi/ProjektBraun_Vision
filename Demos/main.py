import cv2 as cv

print(cv.__version__)

from PyQt5.QtWidgets import *
app = QApplication([])
label = QLabel('Hello World!')
label.show()
app.exec_()