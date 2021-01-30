import cv2 as cv
import numpy as np
import time

video = cv.VideoCapture(0)

for i in range(60):
    global background
    isTrue,background = video.read()
    cv.imshow("scanning",background)
    if isTrue==0:
        break
background = cv.flip(background,1)
isTrue=1
while isTrue==1:
    isTrue,frame = video.read()
    frame=cv.flip(frame,1)
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

    lower_red = np.array([100,85,100])
    upper_red = np.array([100,255,255])
    mask1 = cv.inRange(hsv,lower_red,upper_red)
    lower_red = np.array([155,90,100])
    upper_red = np.array([180,255,255])
    mask2 = cv.inRange(hsv,lower_red,upper_red)

    mask1 = mask1+mask2
    kernel = np.ones((3,3),np.uint8)
    mask1 = cv.morphologyEx(mask1,cv.MORPH_OPEN,kernel,iterations=2)
    mask1 = cv.morphologyEx(mask1,cv.MORPH_CLOSE,kernel,iterations=2)
    dilate=cv.dilate(mask1,kernel,iterations=2)
    mask2 = cv.bitwise_not(mask1)
    res1 = cv.bitwise_and(background,background,mask=mask1)
    res2 = cv.bitwise_and(frame,frame,mask=mask2)
    output = cv.addWeighted(res1,1,res2,1,0)
    cv.imshow("output",output)
    if cv.waitKey(1) & 0xFF==ord('a'):
        break
video.release()
cv.destroyAllWindows()