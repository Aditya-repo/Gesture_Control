import cv2
import numpy as np
import copy
import math
import action_maker

# parameters
cap_region_x_begin = 0.5  # start point/total width
cap_region_y_end = 0.9  # start point/total width
threshold = 60  # BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 50
learningRate = 0

# variables
isBgCaptured = 0  # bool, whether the background captured
triggerSwitch = False  # if true, keyborad simulator works

def printThreshold(thr):
	print("! Changed threshold to " + str(thr))


def removeBG(frame):
	fgmask = bgModel.apply(frame, learningRate=learningRate)
	# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
	# res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

	kernel = np.ones((3, 3), np.uint8)
	fgmask = cv2.erode(fgmask, kernel, iterations=1)
	res = cv2.bitwise_and(frame, frame, mask=fgmask)
	return res


def calculateFingers(res, drawing):  # -> finished bool, cnt: finger count
	#  convexity defect
	hull = cv2.convexHull(res, returnPoints=False)
	if len(hull) > 3:
		defects = cv2.convexityDefects(res, hull)
		if type(defects) != type(None):  # avoid crashing.   (BUG not found)
			cnt = 0
			for i in range(defects.shape[0]):  # calculate the angle
				s, e, f, d = defects[i][0]
				start = tuple(res[s][0])
				end = tuple(res[e][0])
				far = tuple(res[f][0])
				a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
				b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
				c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
				angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
				if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
					cnt += 1
					cv2.circle(drawing, far, 8, [211, 84, 0], -1)
			return True, cnt
	return False, 0


def movement_cap(res):
	M = cv2.moments(res)
	Cx = int(M['m10'] / M['m00'])
	Cy = int(M['m01'] / M['m00'])
	return Cx, Cy

def reset_bg():
	bgModel = None
	triggerSwitch = False
	isBgCaptured = 0
	print('!!!Reset BackGround!!!')

# Camera
camera = cv2.VideoCapture(0)
camera.set(10, 200)
cv2.namedWindow('trackbar')
cv2.createTrackbar('trh1', 'trackbar', threshold, 100, printThreshold)

while camera.isOpened():
	ret, frame = camera.read()
	threshold = cv2.getTrackbarPos('trh1', 'trackbar')
	frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
	frame = cv2.flip(frame, 1)  # flip the frame horizontally
	cv2.rectangle(frame,
				  (int(cap_region_x_begin * frame.shape[1]), 0),
				  (frame.shape[1], int(cap_region_y_end * frame.shape[0])),
				  (255, 0, 0),
				  2)
	cv2.imshow('original', frame)

	#  Main operation
	if isBgCaptured == 1:  # this part wont run until background captured
		img = removeBG(frame)
		img = img[0:int(cap_region_y_end * frame.shape[0]),
			  int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI
		#cv2.imshow('mask', img)

		# convert the image into binary image
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
		cv2.imshow('blur', blur)
		ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
		#cv2.imshow('ori', thresh)

		# get the coutours
		thresh1 = copy.deepcopy(thresh)
		contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		length = len(contours)
		maxArea = -1
		if length > 0:
			res = max(contours, key=lambda x: cv2.contourArea(x))
			hull = cv2.convexHull(res)
			drawing = np.zeros(img.shape, np.uint8)
			cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
			cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

			isFinishCal, cnt = calculateFingers(res, drawing)
			#com_x, com_y = movement_cap(res)
			#cv2.circle(drawing, (com_x, com_y), 10, [200, 255, 109], -1)
			if isFinishCal is True:
				print(cnt)
				action_maker.initAction(cnt)
		cv2.imshow('output', drawing)

	# Keyboard OP
	k = cv2.waitKey(10)
	if k == 27:  # press ESC to exit
		camera.release()
		cv2.destroyAllWindows()
		break
	elif k == ord('b'):  # press 'b' to capture the background
		bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
		isBgCaptured = 1
		print('!!!Background Captured!!!')
	elif k == ord('r'):  # press 'r' to reset the background
		reset_bg()
	elif k == ord('n'):
		triggerSwitch = True
		print('!!!Trigger On!!!')