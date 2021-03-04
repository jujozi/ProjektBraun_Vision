import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
import cv2 as cv
import sys
print(cv.__version__)


img = cv.imread("DSC01873.JPG")
if img is None:
    sys.exit("Could not read the image.")
cv.imshow("Display window", img)
k = cv.waitKey(0)
if k == ord("s"):
    cv.imwrite("starry_night.png", img)


