import numpy as np
import cv2 as cv
def nothing(x):
    print(str(x))
# Create a black image, a window

cv.namedWindow('Settings')
# create trackbars for color change
test = 5
cv.createTrackbar('Settings','Settings',test,255,nothing)

img = cv.imread('klemmbaustein-2x2.jpg')
while(1):
    cv.imshow('Settings',img)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()