'''
Documentation: This is a demonstration of OpenCV's face-tracking and camshift cababilities.

Julius Rajala @2015
'''
class App(object):
    def __init__(self, video_src):
        self.cam = cv2.VideoCapture(video_src)
        self.running = True
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.trackingState = 0
        self.searchingFace = True
        self.keyPresses = { 
                            27:self.quit,
                            ord('f'):self.enableFaceSearch
                           }
    def enableFaceSearch(self):
        self.searchingFace = True
        self.trackingState = 0

    def quit(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def detectFaces(self, frame, gray):
        faces = self.face_cascade.detectMultiScale(gray, 1.2, 5)
        face = (0,0,0,0)
        for (x,y,w,h) in faces:
            face = (x,y,w,h)
        return frame, face if len(faces) == 1 else (0,0,0,0) #Conditional operator here

    def trackFaces(self, frame, ret, face):
        x,y,w,h = face

        #Setting up Range of Interest for tracking
        roi = frame[x:x+w, y:y+h]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array((0.,60.,32.)), np.array((180.,255.,255.)))

        #Setting range of interest for the application
        hsv_roi = hsv[y:y+h, x:x+w]
        mask_roi = mask[y:y+h, x:x+w]
        roi_hist = cv2.calcHist([hsv_roi], [0],mask_roi,[180],[0,180])

        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

        #setup the termination criteria, either 10 iteration or move by atleast 1pt
        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0,180],1)
    
        #apply meanshift to get the new location
        ret, (x,y,w,h) = cv2.CamShift(dst, (x,y,w,h), term_crit)

        cv2.ellipse(frame, ret,(0,0,255),2)
        cv2.imshow('img2', frame)

        k = cv2.waitKey(30) & 0xff
        if k in self.keyPresses:
            self.keyPresses[k]()
        
    def run(self):
        while self.cam.isOpened():
            ret, self.frame = self.cam.read()
            self.frame = cv2.flip(self.frame, 1)
            
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            if self.searchingFace:
                frame2, (x,y,w,h) = self.detectFaces(self.frame, gray)
                if (x,y,w,h) != (0,0,0,0):
                    self.trackingState = 1
                    img = cv2.rectangle(self.frame, (x,y),(x+w, y+h),(255,0,0),2)
                    print x, y, x+w, y+h
            
            if self.trackingState == 1:
                self.searchingFace = False
                self.trackFaces(self.frame, ret, (x,y,w,h))
                #Draw circle and stuff
                print "tracking face"

            #print faceCount
            cv2.imshow("AppName", frame2)
            k = cv2.waitKey(30) & 0xff
            if k in self.keyPresses:
                self.keyPresses[k]()

if __name__=="__main__":
    import numpy as np
    import cv2

    print __doc__

    video_src = 0
    App(video_src).run()
