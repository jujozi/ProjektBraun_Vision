import cv2 as cv
import sys
from src import VisionLib as vl

if __name__ == '__main__':

    img = cv.imread("DSC01873.JPG")
    if img is None:
        sys.exit("Could not read the image.")
    cv.imshow("Display window", vl.ResizeWithAspectRatio(img, width=500))




    k = cv.waitKey(0)
    if k == ord("s"):
        cv.imwrite("starry_night.png", img)
    cv.destroyAllWindows()