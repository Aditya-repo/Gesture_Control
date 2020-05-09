import cv2
import numpy as np
import time

def calc_median_frame(cap_list):
    sample_count=len(cap_list)
    sample_list=[]
    for i in list(map(int,sample_count*np.random.uniform(size=25))):
        sample_list.append(cap_list[i])
    median_frame=np.median(sample_list,axis=0).astype(dtype=np.uint8)
    return median_frame



if __name__=='__main__':
    cap=cv2.VideoCapture(0)
    ret=True
    frame_list=[]
    print()
    tst = time.time()
    collect=True
    mf = np.zeros((480,640))
    while(ret):
        ret,frame=cap.read()
        gframe=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        if collect:
            frame_list.append(frame)
        ttst = time.time()
        cv2.imshow('feed',frame)
        #print(ttst,type(ttst))
        if ttst-tst >= 3.75 and ttst-tst<4.0:#
            mf = calc_median_frame(frame_list)
            mf = cv2.cvtColor(mf,cv2.COLOR_BGR2GRAY)
            print(mf.shape,gframe.shape)
        if mf.all():
            dif_frame=cv2.absdiff(gframe,mf)
            cv2.imshow('dframe',dif_frame)
            collect = False




        if cv2.waitKey(1)==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    print(len(frame_list))