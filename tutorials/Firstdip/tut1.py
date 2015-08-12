import numpy as np
import cv2

#Capturing webcam video to be manipulated at a later date.
cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()

    #Turning video to grayscale
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #displaying resulting frame
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
