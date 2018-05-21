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

pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture("video/60fps480p.mp4")
 
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])


while True:
	(grabbed, frame) = camera.read()
	
	grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blurredGrayFrame = cv2.GaussianBlur(grayFrame,(5, 5),0)
	
	low_threshold = 50
	high_threshold = 200
	edges = cv2.Canny(blurredGrayFrame, low_threshold, high_threshold)

	cv2.imshow("edges", edges)
	
	rho = 1  # distance resolution in pixels of the Hough grid
	theta = 3.14#np.pi / 180  # angular resolution in radians of the Hough grid
	threshold = 15  # minimum number of votes (intersections in Hough grid cell)
	min_line_length = 100  # minimum number of pixels making up a line
	max_line_gap = 20  # maximum gap in pixels between connectable line segments
	line_image = np.copy(frame) * 0  # creating a blank to draw lines on

	# Run Hough on edge detected image
	# Output "lines" is an array containing endpoints of detected line segments
	lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
						min_line_length, max_line_gap)
	
	i = 0
						
	for line in lines:
		for x1,y1,x2,y2 in line:
			i = i + 1
			if i > 10: break
			cv2.line(line_image,(x1,y1),(x2,y2),(255,255,0), 3)
			
	# Draw the lines on the image
	lines_edges = cv2.addWeighted(frame, 0.8, line_image, 1, 0, frame)
 
	# show the frame to our screen
	cv2.imshow("frame", frame)
	key = cv2.waitKey(1) & 0xFF
        
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
		
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
