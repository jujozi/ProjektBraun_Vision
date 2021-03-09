import cv2 as cv
import os

devs = os.listdir('/dev')
devsVideo = []
for dev in devs:
    if dev.startswith('video'):
        devsVideo.append(dev)
print(devsVideo)

cap = cv.VideoCapture(2)

while 1:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")

    try:
        cv.imshow('image', frame)
    except:
        print('fuck')

    k = cv.waitKey(20) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()