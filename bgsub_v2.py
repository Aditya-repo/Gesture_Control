import numpy as np
import cv2

cap = cv2.VideoCapture(0)
subtractor=cv2.createBackgroundSubtractorMOG2()

while True:
    _,frame=cap.read()
    cv2.flip(frame,1,frame)
    fmask=subtractor.apply(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #subtacting the fg from bg
    result = cv2.bitwise_and(gray,gray,mask=fmask)

    cv2.imshow("Frame",frame)
    cv2.imshow("result",result)

    if cv2.waitKey(30)&0xFF==27:
        break

cap.release()
cv2.destroyAllWindows()
