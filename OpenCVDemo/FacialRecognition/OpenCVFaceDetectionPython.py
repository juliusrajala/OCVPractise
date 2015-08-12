import numpy as np
import cv2

keyPresses = {
    27:quit
    }

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def detectFaces(frame, gray):
    global face_cascade
    global eye_cascade


    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    face = (0,0,0,0)
    for (x,y,w,h) in faces:
        face = (x,y,w,h)
        img = cv2.rectangle(frame, (x,y),(x+w, y+h),(255,0,0),2)
    return frame, face if len(faces) == 1 else (0,0,0,0) #Conditional operator here

def main():
    global vid
    vid = cv2.VideoCapture(0)

    while(vid.isOpened()):
        ret, frame = vid.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame, (x,y,w,h) = detectFaces(frame, gray)
        if (x,y,w,h) != (0,0,0,0):
            print x, y, x+w, y+h
        #print faceCount

        cv2.imshow("AppName", frame)
        k = cv2.waitKey(30) & 0xff
        if k in keyPresses:
            keyPresses[k](frame)
        

__name__=="__main__" and main()