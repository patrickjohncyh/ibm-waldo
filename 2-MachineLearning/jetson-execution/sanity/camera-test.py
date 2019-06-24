import cv2
import time

capture = cv2.VideoCapture('testvid.mp4')
while (capture.isOpened()):
    ret,frame = capture.read()
    stime = time.time()
    if ret :
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q') :
            break
        print( str(1.0/(time.time()-stime)) + "FPS")
    else:
        break
capture.release()
