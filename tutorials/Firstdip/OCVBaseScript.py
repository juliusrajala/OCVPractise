import numpy as np
import cv2
import time

def quit(self):
	cv2.destroyAllWindows()
	vid.release()

def screenCap(frame):
	print "Taking a screen capture"
	cv2.imwrite("s"+(time.strftime("%H:%M:%S"))+".jpg", frame)	

keyPresses = {
	27:quit,
	ord("p"): screenCap
}

def main():
	global vid
	vid = cv2.VideoCapture(0)
	while(vid.isOpened()):
		ret, frame = vid.read()
		frame = cv2.flip(frame, 1)
		
		#Place wanted operations here
		
		cv2.imshow('AppName', frame)
		
		k = cv2.waitKey(30) & 0xff
		if k in keyPresses:
			keyPresses[k](frame)
		
__name__ == "__main__" and main()