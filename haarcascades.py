import cv2

hand_cascade=cv2.CascadeClassifier('palm.xml')

cap=cv2.VideoCapture(0)

while True:
    _,frame=cap.read()
    frame=cv2.flip(frame,1)
    show=frame.copy()
    hand=hand_cascade.detectMultiScale(frame,1.3,5)
    area=0
    X=Y=W=H=0
    for (x,y,w,h) in hand:
        if w*h>area:
            area=w*h
            X,Y,W,H=x,y,w,h
    if area>0:
        cv2.rectangle(show,(X,Y),(X+W,Y+H),(0,230,30),1)

    cv2.imshow('live_feed',show)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break


cap.release()
cv2.destroyAllWindows()