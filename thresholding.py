import cv2
import numpy as np

img= cv2.imread('sample_right_hand.jpg')
lower = np.array([0, 48, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")

img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
skin=cv2.inRange(img_hsv,lower,upper)
skin=skin.astype('uint8')
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
skin = cv2.erode(skin, kernel, iterations=2)
skin = cv2.dilate(skin, kernel, iterations=2)

template=skin
w,h=template.shape[::-1]
img2=cv2.imread('sample3.jpg')
img2_hsv=cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)
thr=cv2.inRange(img2_hsv,lower,upper)
thr=thr.astype("uint8")

result=cv2.matchTemplate(thr,template,cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

print(max_val,max_loc)
print(np.where(result>=0.45))
cv2.rectangle(img2,max_loc,(max_loc[0]+w,max_loc[1]+h),(0,255,255),2)
cv2.imshow('template',skin)
cv2.imshow('major_thr',thr)
cv2.imshow('detected',img2)

cv2.waitKey(0)
cv2.destroyAllWindows()