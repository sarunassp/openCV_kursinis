import sys
import cv2
import numpy as np
import time

# Set up tracker.
# Instead of MIL, you can also use

tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
tracker_type = tracker_types[2]

if tracker_type == 'BOOSTING':
    tracker = cv2.TrackerBoosting_create()
if tracker_type == 'MIL':
    tracker = cv2.TrackerMIL_create()
if tracker_type == 'KCF':
    tracker = cv2.TrackerKCF_create()
if tracker_type == 'TLD':
    tracker = cv2.TrackerTLD_create()
if tracker_type == 'MEDIANFLOW':
    tracker = cv2.TrackerMedianFlow_create()
if tracker_type == 'GOTURN':
    tracker = cv2.TrackerGOTURN_create()

# Read video
video = cv2.VideoCapture("video/60fps480p.mp4")

# Exit if video not opened.
if not video.isOpened():
    print "Could not open video"
    sys.exit()

# Read first frame.
ok, frame = video.read()
if not ok:
    print 'Cannot read video file'
    sys.exit()

colorLower = (16, 140, 120)
colorUpper = (22, 230, 220)

#222.5 217 5.59

# Define an initial bounding box
bbox = (220, 215, 20, 20)

# Uncomment the line below to select a different bounding box
#bbox = cv2.selectROI(frame, False)

frameCount = 0
colorCount = 0
trackerCount = 0


ok, frame = video.read()
frame = cv2.GaussianBlur(frame, (5, 5), 0)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, colorLower, colorUpper)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)
cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
if len(cnts) > 0:
    areas = [cv2.contourArea(c) for c in cnts]
    max_index = np.argmax(areas)
    cnt=cnts[max_index]
    bbox = cv2.boundingRect(cnt)
    tracker.init(frame, bbox)
    bbox = (bbox[0]-5, bbox[1]-5, bbox[2] + 10, bbox[3] + 10)
    c = max(cnts, key=cv2.contourArea)
    ((x, y), radius) = cv2.minEnclosingCircle(c)

    # only proceed if the radius meets a minimum size
    if radius > 2:
        colorCount += 1
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 1)

# Initialize tracker with first frame and bounding box
computeTimes = []
count = 0
countTracked = 0
while True:
    if count == 3050:
        break
    start = time.time()
    frameCount += 1
    # Read a new frame
    ok, frame = video.read()
    if not ok:
        break

    # Start timer
    timer = cv2.getTickCount()

    # Update tracker
    ok, bbox = tracker.update(frame)

    # Draw bounding box
    if ok :#and count % 20 != 0:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        trackerCount += 1
        countTracked += 1
    else:
        # Tracking failure
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, colorLower, colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:
            areas = [cv2.contourArea(c) for c in cnts]
            max_index = np.argmax(areas)
            cnt=cnts[max_index]
            bbox = cv2.boundingRect(cnt)
            if tracker_type == 'BOOSTING':
                tracker = cv2.TrackerBoosting_create()
            if tracker_type == 'MIL':
                tracker = cv2.TrackerMIL_create()
            if tracker_type == 'KCF':
                tracker = cv2.TrackerKCF_create()
            if tracker_type == 'TLD':
                tracker = cv2.TrackerTLD_create()
            if tracker_type == 'MEDIANFLOW':
                tracker = cv2.TrackerMedianFlow_create()
            if tracker_type == 'GOTURN':
                tracker = cv2.TrackerGOTURN_create()
            asd = tracker.init(frame, bbox)
            bbox = (bbox[0]-5, bbox[1]-5, bbox[2] + 10, bbox[3] + 10)
            #cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
    
            # only proceed if the radius meets a minimum size
            if radius > 2:
                colorCount += 1
                countTracked += 1
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                #cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 1)
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(frame,[box],0,(0,0,255),2)

        else:
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    # Display tracker type on frame
    cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

    # Display result
    cv2.imshow("Tracking", frame)
    
    end = time.time()
    computeTimes.append(end-start)

    count += 1

    k = cv2.waitKey(1) & 0xff
	if key == ord("q"):
		break

video.release()
cv2.destroyAllWindows()
print ("all frames " + str(frameCount))
print ("tracked frames " + str(countTracked))
print ("color frames " + str(colorCount))
print ("tracker frames " + str(trackerCount))
print (sum(computeTimes)/len(computeTimes))