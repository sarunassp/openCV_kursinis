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
count = 0
# keep looping
while True:
	start = time.time()

	# grab the current frame
	(grabbed, frame) = camera.read()
 
	if not grabbed:
		print "End of video"
		break
 
	# blur it, and convert it to the HSV color space
	#frame = cv2.GaussianBlur(frame, (5, 5), 0)
	#hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# show the frame to our screen
	count += 1
	if count == 2:
		cv2.imwrite("original.jpg", frame)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
