import numpy as np
import cv2
import time
import matplotlib

def quit(self):
	global vid
	if vid.isOpened():
		print "Closing"
		cv2.destroyAllWindows()
		vid.release()

def screenCap(frame):
	print "Taking a screen capture"
	cv2.imwrite("s"+(time.strftime("%H:%M:%S"))+".jpg", frame)	
	
def startHandling(self):
	print "BGS-flipped"
	global started
	if not otsu:
		started = not started
	
def drawCircle():
	x,y,w,h = 400,400,50,50
	
def startOtsu(self):
	global otsu
	global started
	if started:
		otsu = not otsu
		
keyPresses = {
	27:quit,
	ord("p"): screenCap,
	ord("g"): startHandling,
	ord("o"): startOtsu
}

def calculateBoxContent(img):
	count = 0
	for x in range(74):
		for y in range(74):
			if img[x,y] != 0:
				count+=1
	if count > 2000:
		print "Box tapped."
		
def drawHistogram():
		

def main():
	global vid
	global fgbg
	global started
	global otsu
	vid = cv2.VideoCapture(0)
	started = False
	x,y,w,h = 100,100,75,75
	otsu = False
	
	
	fgbg = cv2.createBackgroundSubtractorMOG2(100, 10, False)
	#Main loop for the script
	while(vid.isOpened()):
		ret, frame = vid.read()
		
		#Place wanted operations here
		if started:
			frame = fgbg.apply(frame)
			frame = cv2.bilateralFilter(frame, 9, 75, 75)
		
		if otsu:
			blur = cv2.GaussianBlur(frame,(5,5),0)
			ret3, frame = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
			calculateBoxContent(frame[x:x+w,y:y+h])
		
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
		
		frame = cv2.flip(frame, 1)
		cv2.imshow('AppName', frame)
		
		k = cv2.waitKey(30) & 0xff
		if k in keyPresses:
			keyPresses[k](frame)
	quit(1)
		
__name__ == "__main__" and main()