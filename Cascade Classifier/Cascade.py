import cv2
import numpy as np

hand_cascade = cv2.CascadeClassifier('3_stage_hand_cascade.xml')
cap = cv2.VideoCapture(0)
min_size=float('inf')
max_size=0
while True:
    _,frame=cap.read()
    cv2.flip(frame,1,frame)
    cv2.resize(frame,(800,800),frame)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    hands = hand_cascade.detectMultiScale(gray,1.3,6)

    for (x,y,w,h) in hands:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        if w*h > max_size:
            max_size=w*h
        if w*h<min_size:
            min_size=w*h
    cv2.imshow('feed',frame)

    if cv2.waitKey(1)==ord('q'):
        break
print('max area detected={0}\nminimum area detected={1}'.format(max_size,min_size))
cap.release()
cv2.destroyAllWindows()
