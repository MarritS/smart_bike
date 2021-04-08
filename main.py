# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 16:05:14 2021

@author: marri
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 21:07:14 2021

@author: marri
"""
import cv2
import yolo
from imutils.video import FPS
from tracker import KCFTracker
import winsound


SAVE_VIDEO_TRACKING = True
SAVE_VIDEO_DETECTION = True
SHOW_TRACKING = True
SHOW_DETECTION = False
FRAMERATE = 10
INPUT_FILE="00105.MTS"
OUTPUT_FILE_TRACKING = "result_tracking.mp4"
OUTPUT_FILE_DETECTION = "result_detection.mp4"

fps = FPS().start()
mp3File = "bell.wav"
fourcc = cv2.VideoWriter_fourcc(*"MJPG")

vs = cv2.VideoCapture(INPUT_FILE)
writerTracking = cv2.VideoWriter(OUTPUT_FILE_TRACKING, fourcc, 30,
        (800, 600), True)
writerDetection = cv2.VideoWriter(OUTPUT_FILE_DETECTION, fourcc, 30,
        (800, 600), True)


cnt=0
frameskip = 30/FRAMERATE
bellcnt=0


size=0
oldsize=0
box = (0,0,0,0)
count_increase=0

tracker = KCFTracker(True, True, True)
init=False
tracking=True


def tracking_cars():
        if tracking_cars.tracking:
            box = tracker.update(frame_tracking)
            #Turn list into integers
            box = list(map(int, box))
           
            size = box[2]*box[3]
            print(size)
    
            if size<=(tracking_cars.old_size):
                tracking_cars.count_no_increase +=1
            else:
                tracking_cars.count_no_increase = 0
                
            if (tracking_cars.count_no_increase>=8):
                tracking_cars.tracking=False
            if (tracking_cars.count_no_increase>=4 and size > 4000):
                tracking_cars.tracking=False
        
            print(tracking_cars.count_no_increase)
            
            p1 = (int(box[0]), int(box[1]))
            p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
            cv2.rectangle(frame_tracking, p1, p2, (255, 0, 0), 2, 1)
            tracking_cars.old_size = size
            #oldsize = size 
        
        return frame_tracking
tracking_cars.count_no_increase=0
tracking_cars.old_size=0
tracking_cars.tracking=True

while True:
        bellcnt+=1
        cnt+=1
        
        try:
            (grabbed, frame) = vs.read()
        except:
            break
        if frame is None:
            break
        
        frame_tracking = frame.copy()
        frame_detection = frame.copy()
        fps.update()
        
          
        if init is True and tracking is True and cnt==frameskip:
            frame_tracking = tracking_cars()
            if SHOW_TRACKING:
                cv2.imshow("Tracking", frame_tracking)
                key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if SAVE_VIDEO_TRACKING:
               frame_tracking = cv2.resize(frame_tracking, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
               writerTracking.write(cv2.resize(frame_tracking,(800, 600)))
    
        if cnt == frameskip:
            
            cnt=0
            boxes, frame_detection = yolo.find_vehicles(frame_detection, tiny=True)
            sizes = []
            for box in boxes:
                size = (box[2]*box[3])
                sizes.append(size)
                if init is False:
                    init = True
                    tracker.init(box, frame_detection)
                    

            if len(sizes)>0:
                if (max(sizes)>30000 and bellcnt>8):
                    print('car')
                    winsound.PlaySound(mp3File, winsound.SND_ASYNC | winsound.SND_ALIAS )
                    bellcnt=0
                    
            if SAVE_VIDEO_DETECTION:    
                frame_detection = cv2.resize(frame_detection, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
                writerDetection.write(cv2.resize(frame_detection,(800, 600)))
            if SHOW_DETECTION:
                cv2.imshow('detection', frame_detection)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                   break
                
                
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            
        else: 
            if size is not None:
                if SAVE_VIDEO_TRACKING:
                    frame_tracking = cv2.resize(frame_tracking, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
                    writerTracking.write(cv2.resize(frame_tracking,(800, 600)))
                if SAVE_VIDEO_DETECTION:    
                    frame_detection = cv2.resize(frame_detection, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
                    writerDetection.write(cv2.resize(frame_detection,(800, 600)))
       
        

       
               
        
         
fps.stop()

print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()

# release the file pointers
print("[INFO] cleaning up...")
writerTracking.release()
writerDetection.release()
vs.release()
    
        #cv2.imshow('Input', img)