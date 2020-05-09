import cv2
import time

cap = cv2.VideoCapture(0)

start=time.time()

for i in range(0,120):
    _,frame=cap.read()

end=time.time()

print(float(120)/(end-start))

#while True:
  #  _, frame = cap.read()
  #  frame = cv2.flip(frame, 1)
  #  cv2.imshow('view',frame)
  #  if cv2.waitKey(1)&0xFF==ord('q'):
  #      cv2.imwrite('sample4.jpg',frame)
  #      break

#cv2.imwrite('bh.jpg',frame)
cap.release()
#cv2.destroyAllWindows()