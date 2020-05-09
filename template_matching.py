import numpy as np
import cv2
import os

def alarm():
    global c
    c=0
    duration=1
    freq=440
    if c<1:
        os.system('play -nq -t alsa synth {} sine {}'.format(duration,freq))
        c=c+1
    pass

def detect_face(frame):
    '''detects face and retuens coordinates that can
    be used to delete the face from the frame'''
    face_casc=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    face=face_casc.detectMultiScale(frame,1.3,5)
    area=0
    X=Y=W=H=0
    for (x,y,w,h) in face:
        if w*h>area:
            area=w*h
            X,Y,W,H=x,y,w,h
    if area>0:
        return [X,Y,W,H,1]
    else:
        return [X,Y,W,H,0]

def threshold(frame):
    '''thresholding to extract skin colour'''
    lower = np.array([0, 48, 80], dtype="uint8")
    upper = np.array([20, 255, 255], dtype="uint8")
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skin = cv2.inRange(img_hsv, lower, upper)
    return skin

def match_template(frame):
    template=cv2.imread('sample_right_hand.jpg')
    hand=threshold(template)
    hand=hand.astype('uint8')
    w, h = hand.shape[::-1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    skin = cv2.erode(hand, kernel, iterations=2)
    skin = cv2.dilate(hand, kernel, iterations=2)

    result = cv2.matchTemplate(frame,skin, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_val, max_loc, (max_loc[0] + w, max_loc[1] + h)

def countouring(frame,location):
    top=location[0][1]
    bottom=location[1][1]
    left=location[0][0]
    right=location[1][0]
    segment=frame[top:bottom,left:right]

    k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    cv2.erode(segment,k,segment,iterations=2)
    cv2.dilate(segment,k,segment,iterations=7)
    cv2.medianBlur(segment,7,segment)

    cv2.imshow('contouring',segment)
    cntours, _ = cv2.findContours(segment.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cntours) == 0:
        return
    else:
        segmented = max(cntours, key=cv2.contourArea)
        return segmented

if __name__=='__main__':
    img = cv2.imread('hand2.jpg')
    img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    feed=cv2.VideoCapture(0)
    frame_number=0
    cur_hand_area = 0
    while True:
        _,frame=feed.read()
        cv2.flip(frame,1,frame)
        show_fr=frame.copy()# frame on which all information will be shown.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        x,y,w,h,present = detect_face(gray)
        if present:# if face is detected
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),-1) #subtracting the face from the frame
        copy= threshold(frame)
        copy=copy.astype('uint8')

        #template matching
        roi = match_template(copy)

        if roi[0]>=0.4:
            cv2.rectangle(show_fr,roi[1],roi[2],(0,255,0),2)
            hand=countouring(copy,(roi[1],roi[2]))
            if hand is not None:
                cv2.drawContours(show_fr,[hand+roi[1]],-1,(0,0,255),2)
                #trying to detect closing/opening of fist
                hand_area=cv2.contourArea(hand)
                if (frame_number%20)==0:
                    if hand_area>cur_hand_area:
                        print('opening')
                        cur_hand_area=hand_area
                    elif hand_area < cur_hand_area:
                        print('closing')
                        cur_hand_area=hand_area

        cv2.imshow('live feed',show_fr)
        cv2.imshow('processed',copy)
        if cv2.waitKey(1)&0xFF==27:
            break
        frame_number=frame_number+1
    feed.release()
    cv2.destroyAllWindows()