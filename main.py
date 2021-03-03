import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
import cv2 as cv
import sys
print(cv.__version__)


def ResizeWithAspectRatio(image, width=None, height=None, inter=cv.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv.resize(image, dim, interpolation=inter)


if __name__ == '__main__':
    img = cv.imread("DSC01873.JPG")
    if img is None:
        sys.exit("Could not read the image.")
    cv.imshow("Display window", ResizeWithAspectRatio(img, width=500))
    k = cv.waitKey(0)
    if k == ord("s"):
        cv.imwrite("starry_night.png", img)