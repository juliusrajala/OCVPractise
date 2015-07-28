import numpy as np
import cv2
import time
from matplotlib import pyplot as plt
from pytify import Spotify
spotify = Spotify()

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
		
def displayHistogram(frame):
	histr = cv2.calcHist([frame], [0], None, [10], [0,256])
	bin_count = histr.shape[0]
	bin_w = 24
	img = np.zeros((256, bin_count*bin_w*100,3), np.uint8)
	for i in xrange(bin_count):
		h = int(histr[i])
		cv2.rectangle(img, (i*bin_w+20, 100), ((i+1)*bin_w-0, 100-h), (int(180.0*i/bin_count), 255, 255), -1)
	img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
	cv2.imshow('hist', histr)
		
keyPresses = {
	27:quit,
	ord("p"): screenCap,
	ord("g"): startHandling,
	ord("o"): startOtsu
}

def calculateBoxContent(img, spot):
	global totHits
	global spotify
	count = 0
	for x in range(0,75):
		for y in range(0,75):
			if img[x,y] != 0:
				count+=1
	if count > 2000:
		totHits +=1
		spotify.next()
		print "Box tapped at: " + spot
		# print "Box tapped "+ str(totHits) +" times!"
	elif count > 2000 and spot[0] == "r":
		print "Next song"
		

#function checks if the screen simply flashes white to avoid mishits
def checkSnowBlindness(frame):
	img = frame[0:50, 200:250]
	count = 0
	for x in range(50):
		for y in range(50):
			if img[x,y] != 0:
				count+=1
	if count > 300:
		print "Screen flashed, no count."
		return True
	else:
		return False
		
def main():
	global vid
	global fgbg
	global started
	global otsu
	global totHits
	totHits = 0
	vid = cv2.VideoCapture(0)
	ret, cap = vid.read()
	started = False
	x,y,w,h = 0,0,75,75
	x1,y1 = 640-75, 480-75
	x2,y2 = 0, 480-75
	x3,y3 = 640-75, 0
	otsu = False
	
	
	fgbg = cv2.createBackgroundSubtractorMOG2(100, 10, False)
	#Main loop for the script
	while(vid.isOpened()):
		ret, img = vid.read()
		frame = img
		#Place wanted operations here
		if started:
			frame = fgbg.apply(frame)
			frame = cv2.bilateralFilter(frame, 9, 75, 75)
		
		if otsu:
			blur = cv2.GaussianBlur(frame,(7,7),0)
			ret3, frame = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
			if not checkSnowBlindness(frame):
				calculateBoxContent(frame[x:x+w,y:y+h], "Right top")
				calculateBoxContent(frame[y1:y1+w,x1:x1+h], "Left bottom")
				calculateBoxContent(frame[y2:y2+h,x2:x2+w], "Right bottom")
				calculateBoxContent(frame[y3:y3+w,x3:x3+h], "Left top")

		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),1)
		cv2.rectangle(frame,(x1,y1),(x1+w,y1+h),(255,255,0),1)
		cv2.rectangle(frame,(x2,y2),(x2+w,y2+h),(255,255,0),1)
		cv2.rectangle(frame,(x3,y3),(x3+w,y3+h),(255,255,0),1)
		
		frame = cv2.flip(frame, 1)
		cv2.imshow('AppName', frame)
		
		k = cv2.waitKey(30) & 0xff
		if k in keyPresses:
			keyPresses[k](frame)
	quit(1)
		
__name__ == "__main__" and main()