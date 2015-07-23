import numpy as np
import cv2

cap = cv2.VideoCapture(0)

#Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#Here you need to support the specific videocodex you use for the capture (fourcc)
#Instead of fourcc, -1 means that we're manually selecting codec for this video,
#instead of using fourcc as suggested by tutorial
out = cv2.VideoWriter('output1.avi', fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame, 1)

        #writing the flipped frame
        out.write(frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
