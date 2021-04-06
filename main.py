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
from imutils.video import VideoStream
from playsound import playsound
from tracker import KCFTracker
import winsound
import time


SAVE_VIDEO = True

fps = FPS().start()
mp3File = "bell.wav"
INPUT_FILE="00105.MTS"
fourcc = cv2.VideoWriter_fourcc(*"MJPG")

vs = cv2.VideoCapture(INPUT_FILE)
writer = cv2.VideoWriter("result.mp4", fourcc, 30,
        (800, 600), True)
cnt=0
bellcnt=0
framecnt=0
minsize = 200000
maxsize = 0
size=0
oldsize=0
box = (0,0,0,0)
count_increase=0
tracker = KCFTracker(True, True, True)
init=False
tracking=True
while True:
        #print('Min: ', minsize)
        #print('Max: ', maxsize)
        framecnt+=1
        bellcnt+=1
        cnt+=1
        #print ("Frame number", framecnt)
        try:
            (grabbed, frame) = vs.read()
        except:
            break
        if frame is None:
            break
        
        frame_clean = frame.copy()
        fps.update()
          
        if init is True and tracking is True and cnt==3:
             bbox = tracker.update(frame)
             bbox = list(map(int, bbox))
    # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    
     # Tracking success
             p1 = (int(bbox[0]), int(bbox[1]))
             size = bbox[2]*bbox[3]
             if size>oldsize:
                 count_increase += 1
             elif size<(oldsize-3):
                 count_increase -= 1
             print(count_increase)
             p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
             cv2.rectangle(frame_clean, p1, p2, (255, 0, 0), 2, 1)
             oldsize = size
  
    
        if cnt == 3:
            cnt=0
            
            boxes, img = yolo.find_vehicles(frame, tiny=True)
            cv2.imshow("Tracking", frame_clean)
            sizes = []
            for box in boxes:
                size = (box[2]*box[3])
                sizes.append(size)
                if init is False:
                    init = True
                    tracker.init(box, frame)
                    oldsize = size
                    #tracker.init((40, 40, 90, 90), frame)
                    
                
             
              
            

        # Put FPS
        #cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

            cv2.imshow("Tracking", frame_clean)
            #img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            #cv2.imshow("output", cv2.resize(img,(800, 600)))
            if len(sizes)>0:
                #print('Closest car:', max(sizes))
                if (max(sizes)>30000 and bellcnt>8):
                    print('car')
                    #playsound(mp3File)
                    winsound.PlaySound(mp3File, winsound.SND_ASYNC | winsound.SND_ALIAS )
                    bellcnt=0
            writer.write(cv2.resize(frame_clean,(800, 600)))
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            #cv2.waitKey()
        else: 
            if size is not None:
                #print('blub')
                x = int(box[0])
                y = int(box[1])
                x_plus_w = int(box[0] + box[2])
                y_plus_h = int(box[1] + box[3])
                color = (100, 100, min(size/100, 255))
                #cv2.rectangle(frame, (x, y), (x_plus_w, y_plus_h), color, 2)
                frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
                #cv2.imshow("output", cv2.resize(frame,(800, 600)))
                writer.write(cv2.resize(frame_clean,(800, 600)))
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                   break
                #cv2.waitKey()
                
        
        
        
         
fps.stop()

print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()

# release the file pointers
print("[INFO] cleaning up...")
writer.release()
vs.release()
    
        #cv2.imshow('Input', img)