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
    bbox = (bbox[0]-5, bbox[1]-5, bbox[2] + 10, bbox[3] + 10)
    c = max(cnts, key=cv2.contourArea)
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    # only proceed if the radius meets a minimum size
    if radius > 2:
        colorCount += 1
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 1)


# Initialize tracker with first frame and bounding box

while True:
    frameCount += 1
    # Read a new frame
    ok, frame = video.read()
    if not ok:
        break

    # Start timer
    timer = cv2.getTickCount()

    # Update tracker
    ok, bbox = tracker.update(frame)

    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    # Draw bounding box
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        trackerCount += 1
    else :
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
            bbox = (bbox[0]-5, bbox[1]-5, bbox[2] + 10, bbox[3] + 10)
            tracker.init(frame, bbox)
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    
            # only proceed if the radius meets a minimum size
            if radius > 2:
                colorCount += 1
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

    # Display FPS on frame
    cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

    # Display result
    cv2.imshow("Tracking", frame)

    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break

print (frameCount)
print (colorCount)
print (trackerCount)