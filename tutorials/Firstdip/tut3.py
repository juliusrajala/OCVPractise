#-*- coding: utf-8 -*-
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

#Getting the first frame of the video
ret,frame = cap.read()

#initial hardcoded values for location
# järjestys: etäisyys vasen yläkulma = r, korkean sivun pituus = h
#
r,h,c,w = 150,50,150,50
track_window = (c,r,w,h)

#Setting up range of interest for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0.,60.,32.)), np.array((180., 255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0], mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist,0,255,cv2.NORM_MINMAX)

#Setup the termination criteria either 10 iteration, or move by atleast 1p
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
switch = False

def moveLeft():
    global x
    print "Left"
    if x >= 50:
        x-=50

def moveRight():
    global x
    print x
    if x <= 590:
        x+=50

def moveDown():
    global y
    if y <= 430:
        y+=50
def moveUp():
    global y
    if y >= 50:
        y-=50


control_dict = {
    ord("j"):moveLeft,
    ord("l"):moveRight,
    ord("k"):moveDown,
    ord("i"):moveUp
}


while(1):
    ret, frame = cap.read()
    if ret == True:

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0,180],1)

        #apply meanshift to get new location
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        # x,y,w,h = track_window
        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        img2 = cv2.polylines(frame,[pts], True, 255, 2)

        # img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        cv2.imshow('img2', img2)

        #Drawing on image

        k = cv2.waitKey(60) & 0xff
        if k in control_dict:
            print "Move action ordered."
            control_dict[k]()

        if k == ord('s'):
            switch = True
            print "Started"

        # if cv2.waitKey(1) & 0xff == ord('q'):
        #     break

        if k == 27:
            print "Quit called"
            break

        cv2.imwrite(chr(k)+".jpg", img2)


    else:
        break

cv2.destroyAllWindows()
cap.release()
