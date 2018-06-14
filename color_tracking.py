# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import time
import cv2
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the color
# HSV boundaries  H: 0 - 180, S: 0 - 255, V: 0 - 255 <---- use this
# most people use H: 0 - 360, S: 0 - 100, V: 0 - 100
colorLower = (16, 140, 120)
colorUpper = (22, 230, 220)

pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture("video/60fps480p.mp4")
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])
	
if not camera.isOpened():
	print "Camera not opened"
	exit()

# list for average compute time of frame
computeTimes = []
countAll = 0
countTracked = 0
# keep looping
while True:
	start = time.time()

	# grab the current frame
	(grabbed, frame) = camera.read()
 
	if not grabbed:
		print "End of video"
		break

	countAll += 1
	# blur it, and convert it to the HSV color space
	blurred = cv2.GaussianBlur(frame, (5, 5), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color, then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
 
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
 
		# only proceed if the radius meets a minimum size
		if radius > 2:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			bbox = cv2.boundingRect(c)
			bbox = (bbox[0]-5, bbox[1]-5, bbox[2] + 5, bbox[3] + 5)
			p1 = (int(bbox[0]), int(bbox[1]))
			p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
			cv2.rectangle(frame, p1, p2, (0,255,0), 2, 1)
			countTracked += 1
			#cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
	# if count == 2:
		# cv2.imwrite("finalTracked.jpg", frame)
		# break
	# loop over the set of tracked points
	for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 1.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	end = time.time()
	computeTimes.append(end-start)

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
		
print (sum(computeTimes)/len(computeTimes))

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
print ("all frames " + str(countAll))
print ("tracked frames " + str(countTracked))